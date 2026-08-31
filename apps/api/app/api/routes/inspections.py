import uuid
import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import FileResponse
from app.core.config import get_settings
from app.database import (
    InspectionDocument,
    EvidenceHashes,
    create_inspection,
    get_inspection,
    get_report_path,
    list_inspections,
    delete_inspection,
    save_image_path,
    save_processing_result,
    save_extracted_data,
    save_compliance_results,
    save_report_path,
    save_annotated_image_path,
    save_evidence_hashes,
    reprocess_inspection,
    search_inspections,
)
from app.utils.hashing import hash_bytes, hash_json, hash_file

router = APIRouter()
settings = get_settings()


# ── 1. Create Inspection ──────────────────────────────────────────────
@router.post("", response_model=InspectionDocument)
async def create_inspection_endpoint(
    product_name: str = Query(default=""),
    category: str = Query(default=""),
):
    inspection_id = f"INS-{uuid.uuid4().hex[:8].upper()}"
    doc = InspectionDocument(
        id=inspection_id,
        product_name=product_name or None,
        category=category or None,
    )
    return await create_inspection(doc)


# ── 2. Upload Image ──────────────────────────────────────────────────
@router.post("/{inspection_id}/upload", response_model=InspectionDocument)
async def upload_image_endpoint(inspection_id: str, file: UploadFile = File(...)):
    doc = await get_inspection(inspection_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Inspection not found")

    file_extension = Path(file.filename).suffix if file.filename else ".jpg"
    file_path = settings.upload_dir / f"{inspection_id}{file_extension}"

    content = await file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(content)

    original_hash = hash_bytes(content)

    # Save both the flat evidence_hash and the structured evidence_hashes map
    updated = await save_image_path(inspection_id, str(file_path), original_hash)
    await save_evidence_hashes(
        inspection_id,
        EvidenceHashes(original_image_sha256=original_hash),
    )
    return updated


# ── 3-5. Process Inspection (full pipeline) ──────────────────────────
@router.post("/{inspection_id}/process", response_model=InspectionDocument)
async def process_inspection_endpoint(inspection_id: str):
    doc = await get_inspection(inspection_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Inspection not found")
    if not doc.image_path:
        raise HTTPException(status_code=400, detail="No image uploaded yet")

    from app.graph.workflow import inspection_app

    # Step 3: Vision + OCR pipeline
    await save_processing_result(
        inspection_id,
        pipeline_status="VISION",
        marker_detected=doc.marker_detected,
    )

    initial_state = {"inspection_id": inspection_id, "image_path": doc.image_path}
    final_state = inspection_app.invoke(initial_state)

    # Step 3: Save processing results
    detections = [d.model_dump() if hasattr(d, "model_dump") else d for d in final_state.get("detections", [])]
    ocr_results = [r.model_dump() if hasattr(r, "model_dump") else r for r in final_state.get("ocr_results", [])]
    await save_processing_result(
        inspection_id,
        pipeline_status="OCR_DONE",
        marker_detected=final_state.get("marker_detected", False),
        homography=final_state.get("homography"),
        detections=detections,
        ocr_results=ocr_results,
        measurements=final_state.get("measurements", {}),
    )

    # Step 4: Save extracted product data
    product_data = final_state.get("product_data")
    if product_data:
        pd = product_data.model_dump() if hasattr(product_data, "model_dump") else product_data
        await save_extracted_data(inspection_id, pd)

    # Step 5: Save compliance results
    rule_results = final_state.get("rule_results", [])
    rr = [r.model_dump() if hasattr(r, "model_dump") else r for r in rule_results]
    score = final_state.get("score", 0)
    status = final_state.get("status", "PENDING")
    status_val = status.value if hasattr(status, "value") else status
    await save_compliance_results(inspection_id, rr, score, status_val)

    # Evidence: hash the final result JSON (OCR, measurements, data, rules, score, status)
    result_json = {
        "inspection_id": inspection_id,
        "marker_detected": final_state.get("marker_detected", False),
        "homography": final_state.get("homography"),
        "detections": detections,
        "ocr_results": ocr_results,
        "measurements": final_state.get("measurements", {}),
        "product_data": pd if product_data else None,
        "rule_results": rr,
        "score": score,
        "status": status_val,
    }
    result_hash = hash_json(result_json)
    doc = await get_inspection(inspection_id)
    if doc and doc.evidence_hashes:
        await save_evidence_hashes(
            inspection_id,
            EvidenceHashes(
                original_image_sha256=doc.evidence_hashes.original_image_sha256,
                result_json_sha256=result_hash,
                annotated_image_sha256=doc.evidence_hashes.annotated_image_sha256,
                report_pdf_sha256=doc.evidence_hashes.report_pdf_sha256,
            ),
        )

    return await get_inspection(inspection_id)


# ── 6. Generate / Save Report ─────────────────────────────────────────
@router.post("/{inspection_id}/report")
async def generate_report_endpoint(inspection_id: str):
    from app.reports.generator import generate_inspection_report

    doc = await get_inspection(inspection_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Inspection not found")

    report_path = generate_inspection_report(doc)
    await save_report_path(inspection_id, report_path)

    # Evidence: hash the generated PDF (stored in DB, not inside the PDF itself)
    pdf_hash = hash_file(report_path)
    if doc.evidence_hashes:
        await save_evidence_hashes(
            inspection_id,
            EvidenceHashes(
                original_image_sha256=doc.evidence_hashes.original_image_sha256,
                result_json_sha256=doc.evidence_hashes.result_json_sha256,
                annotated_image_sha256=doc.evidence_hashes.annotated_image_sha256,
                report_pdf_sha256=pdf_hash,
            ),
        )

    return await get_inspection(inspection_id)


# ── Verify Evidence Integrity ─────────────────────────────────────────
@router.get("/{inspection_id}/verify")
async def verify_inspection_endpoint(inspection_id: str):
    from app.utils.hashing import verify_file_hash

    doc = await get_inspection(inspection_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Inspection not found")

    checks = {
        "original_image": {"expected": None, "matches": None},
        "report_pdf": {"expected": None, "matches": None},
    }

    if doc.image_path and Path(doc.image_path).exists() and doc.evidence_hashes.original_image_sha256:
        checks["original_image"]["expected"] = doc.evidence_hashes.original_image_sha256
        checks["original_image"]["matches"] = verify_file_hash(
            doc.image_path, doc.evidence_hashes.original_image_sha256
        )

    if doc.report_path and Path(doc.report_path).exists() and doc.evidence_hashes.report_pdf_sha256:
        checks["report_pdf"]["expected"] = doc.evidence_hashes.report_pdf_sha256
        checks["report_pdf"]["matches"] = verify_file_hash(
            doc.report_path, doc.evidence_hashes.report_pdf_sha256
        )

    return {
        "inspection_id": inspection_id,
        "checks": checks,
        "all_match": all(c["matches"] for c in checks.values() if c["expected"]),
    }


# ── 7. Get One Inspection ────────────────────────────────────────────
@router.get("/{inspection_id}", response_model=InspectionDocument)
async def get_inspection_endpoint(inspection_id: str):
    doc = await get_inspection(inspection_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Inspection not found")
    return doc


# ── 8. List Recent Inspections ────────────────────────────────────────
@router.get("", response_model=list[InspectionDocument])
async def list_inspections_endpoint(
    limit: int = Query(default=20, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
    status: str | None = Query(default=None),
    search: str | None = Query(default=None),
):
    if search or status:
        return await search_inspections(product_name=search, status=status, limit=limit, skip=skip)
    return await list_inspections(limit=limit, skip=skip)


# ── 9. Get Report (PDF) ─────────────────────────────────────────────
@router.get("/{inspection_id}/report")
async def get_report_endpoint(inspection_id: str):
    from app.reports.generator import generate_inspection_report

    doc = await get_inspection(inspection_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Inspection not found")

    report_path = await get_report_path(inspection_id)

    # Generate report on demand if it doesn't exist yet
    if not report_path or not Path(report_path).exists():
        report_path = generate_inspection_report(doc)
        await save_report_path(inspection_id, report_path)
        pdf_hash = hash_file(report_path)
        if doc.evidence_hashes:
            await save_evidence_hashes(
                inspection_id,
                EvidenceHashes(
                    original_image_sha256=doc.evidence_hashes.original_image_sha256,
                    result_json_sha256=doc.evidence_hashes.result_json_sha256,
                    annotated_image_sha256=doc.evidence_hashes.annotated_image_sha256,
                    report_pdf_sha256=pdf_hash,
                ),
            )

    return FileResponse(
        path=report_path,
        media_type="application/pdf",
        filename=f"{inspection_id}.pdf",
    )


# ── Get Original Image ───────────────────────────────────────────────
@router.get("/{inspection_id}/image")
async def get_image_endpoint(inspection_id: str):
    doc = await get_inspection(inspection_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Inspection not found")
    if not doc.image_path or not Path(doc.image_path).exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(path=doc.image_path)


# ── Get Annotated Image ──────────────────────────────────────────────
@router.get("/{inspection_id}/annotated")
async def get_annotated_image_endpoint(inspection_id: str):
    doc = await get_inspection(inspection_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Inspection not found")
    if not doc.annotated_image_path or not Path(doc.annotated_image_path).exists():
        raise HTTPException(status_code=404, detail="Annotated image not found")
    return FileResponse(path=doc.annotated_image_path)


# ── Delete ────────────────────────────────────────────────────────────
@router.delete("/{inspection_id}")
async def delete_inspection_endpoint(inspection_id: str):
    deleted = await delete_inspection(inspection_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Inspection not found")
    return {"deleted": True}


# ── Reprocess ─────────────────────────────────────────────────────────
@router.post("/{inspection_id}/reprocess", response_model=InspectionDocument)
async def reprocess_inspection_endpoint(inspection_id: str):
    doc = await reprocess_inspection(inspection_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Inspection not found")
    return doc
