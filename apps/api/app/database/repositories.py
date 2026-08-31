from datetime import datetime, timezone

from app.database.connection import get_db
from app.database.models import (
    InspectionDocument,
    ExtractedProductData,
    DetectionDoc,
    OCRWordDoc,
    RuleResultDoc,
    EvidenceHashes,
)

COLLECTION = "inspections"


def _doc_from_mongo(data: dict) -> InspectionDocument:
    data["id"] = data.pop("_id")
    return InspectionDocument(**data)


# ── 1. Create Inspection ──────────────────────────────────────────────
async def create_inspection(doc: InspectionDocument) -> InspectionDocument:
    db = get_db()
    now = datetime.now(timezone.utc)
    doc.created_at = now
    doc.updated_at = now
    doc.status = "CREATED"
    payload = doc.model_dump(by_alias=True)
    await db[COLLECTION].insert_one(payload)
    return doc


# ── 2. Save Uploaded Image Path ───────────────────────────────────────
async def save_image_path(
    inspection_id: str,
    image_path: str,
    evidence_hash: str | None = None,
) -> InspectionDocument | None:
    db = get_db()
    update: dict = {
        "image_path": image_path,
        "updated_at": datetime.now(timezone.utc),
    }
    if evidence_hash:
        update["evidence_hash"] = evidence_hash
    await db[COLLECTION].update_one({"_id": inspection_id}, {"$set": update})
    return await get_inspection(inspection_id)


# ── Save Evidence Hashes ──────────────────────────────────────────────
async def save_evidence_hashes(
    inspection_id: str,
    evidence_hashes: EvidenceHashes,
) -> InspectionDocument | None:
    db = get_db()
    await db[COLLECTION].update_one(
        {"_id": inspection_id},
        {"$set": {
            "evidence_hashes": evidence_hashes.model_dump(),
            "hash_algorithm": "SHA-256",
            "hashed_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }},
    )
    return await get_inspection(inspection_id)


# ── 3. Update Processing State ────────────────────────────────────────
async def save_processing_result(
    inspection_id: str,
    pipeline_status: str,
    marker_detected: bool = False,
    homography: list[list[float]] | None = None,
    detections: list[dict] | None = None,
    ocr_results: list[dict] | None = None,
    measurements: dict | None = None,
) -> InspectionDocument | None:
    db = get_db()
    update: dict = {
        "pipeline_status": pipeline_status,
        "marker_detected": marker_detected,
        "updated_at": datetime.now(timezone.utc),
    }
    if homography is not None:
        update["homography"] = homography
    if detections is not None:
        update["detections"] = detections
    if ocr_results is not None:
        update["ocr_results"] = ocr_results
    if measurements is not None:
        update["measurements"] = measurements
    await db[COLLECTION].update_one({"_id": inspection_id}, {"$set": update})
    return await get_inspection(inspection_id)


# ── 4. Save Extracted Product Data ────────────────────────────────────
async def save_extracted_data(
    inspection_id: str,
    product_data: dict,
) -> InspectionDocument | None:
    db = get_db()
    await db[COLLECTION].update_one(
        {"_id": inspection_id},
        {"$set": {
            "product_data": product_data,
            "updated_at": datetime.now(timezone.utc),
        }},
    )
    return await get_inspection(inspection_id)


# ── 5. Save Compliance Results ────────────────────────────────────────
async def save_compliance_results(
    inspection_id: str,
    rule_results: list[dict],
    score: int,
    status: str,
) -> InspectionDocument | None:
    db = get_db()
    await db[COLLECTION].update_one(
        {"_id": inspection_id},
        {"$set": {
            "rule_results": rule_results,
            "score": score,
            "status": status,
            "updated_at": datetime.now(timezone.utc),
        }},
    )
    return await get_inspection(inspection_id)


# ── 6. Save Report Path ──────────────────────────────────────────────
async def save_report_path(
    inspection_id: str,
    report_path: str,
) -> InspectionDocument | None:
    db = get_db()
    await db[COLLECTION].update_one(
        {"_id": inspection_id},
        {"$set": {
            "report_path": report_path,
            "updated_at": datetime.now(timezone.utc),
        }},
    )
    return await get_inspection(inspection_id)


# ── Save Annotated Image Path ─────────────────────────────────────────
async def save_annotated_image_path(
    inspection_id: str,
    annotated_image_path: str,
) -> InspectionDocument | None:
    db = get_db()
    await db[COLLECTION].update_one(
        {"_id": inspection_id},
        {"$set": {
            "annotated_image_path": annotated_image_path,
            "updated_at": datetime.now(timezone.utc),
        }},
    )
    return await get_inspection(inspection_id)


# ── 7. Get One Inspection ────────────────────────────────────────────
async def get_inspection(inspection_id: str) -> InspectionDocument | None:
    db = get_db()
    data = await db[COLLECTION].find_one({"_id": inspection_id})
    return _doc_from_mongo(data) if data else None


# ── 8. List Recent Inspections ────────────────────────────────────────
async def list_inspections(
    limit: int = 20,
    skip: int = 0,
    status: str | None = None,
    search: str | None = None,
) -> list[InspectionDocument]:
    db = get_db()
    query: dict = {}
    if status:
        query["status"] = status
    if search:
        query["product_name"] = {"$regex": search, "$options": "i"}
    cursor = db[COLLECTION].find(query).sort("created_at", -1).skip(skip).limit(limit)
    return [_doc_from_mongo(data) async for data in cursor]


# ── 9. Get Report Path ───────────────────────────────────────────────
async def get_report_path(inspection_id: str) -> str | None:
    db = get_db()
    data = await db[COLLECTION].find_one(
        {"_id": inspection_id},
        {"report_path": 1},
    )
    if data and data.get("report_path"):
        return data["report_path"]
    return None


# ── Generic Update ────────────────────────────────────────────────────
async def update_inspection(
    inspection_id: str,
    updates: dict,
) -> InspectionDocument | None:
    db = get_db()
    updates["updated_at"] = datetime.now(timezone.utc)
    await db[COLLECTION].update_one(
        {"_id": inspection_id},
        {"$set": updates},
    )
    return await get_inspection(inspection_id)


# ── Delete ────────────────────────────────────────────────────────────
async def delete_inspection(inspection_id: str) -> bool:
    db = get_db()
    result = await db[COLLECTION].delete_one({"_id": inspection_id})
    return result.deleted_count > 0


# ── Reprocess (reset for re-run) ──────────────────────────────────────
async def reprocess_inspection(inspection_id: str) -> InspectionDocument | None:
    db = get_db()
    reset_fields = {
        "status": "CREATED",
        "score": None,
        "pipeline_status": None,
        "marker_detected": False,
        "homography": None,
        "detections": [],
        "ocr_results": [],
        "measurements": {},
        "product_data": None,
        "rule_results": [],
        "report_path": None,
        "updated_at": datetime.now(timezone.utc),
    }
    await db[COLLECTION].update_one(
        {"_id": inspection_id},
        {"$set": reset_fields},
    )
    return await get_inspection(inspection_id)


# ── Search / Filter ───────────────────────────────────────────────────
async def search_inspections(
    product_name: str | None = None,
    status: str | None = None,
    category: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    limit: int = 50,
    skip: int = 0,
) -> list[InspectionDocument]:
    db = get_db()
    query: dict = {}
    if product_name:
        query["product_name"] = {"$regex": product_name, "$options": "i"}
    if status:
        query["status"] = status
    if category:
        query["category"] = {"$regex": category, "$options": "i"}
    if date_from or date_to:
        query["created_at"] = {}
        if date_from:
            query["created_at"]["$gte"] = date_from
        if date_to:
            query["created_at"]["$lte"] = date_to
    cursor = db[COLLECTION].find(query).sort("created_at", -1).skip(skip).limit(limit)
    return [_doc_from_mongo(data) async for data in cursor]
