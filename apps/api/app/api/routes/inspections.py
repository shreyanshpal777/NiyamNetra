import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File
from app.core.config import get_settings
from app.models.inspection import InspectionRecord
from app.graph.workflow import inspection_app

router = APIRouter()
settings = get_settings()

# In-memory mock DB until MongoDB is wired up
MOCK_DB: dict[str, InspectionRecord] = {}

@router.post("", response_model=InspectionRecord)
async def create_inspection(file: UploadFile = File(...)):
    inspection_id = f"INS-{uuid.uuid4().hex[:8].upper()}"
    
    # Save uploaded file
    file_extension = Path(file.filename).suffix if file.filename else ".jpg"
    file_path = settings.upload_dir / f"{inspection_id}{file_extension}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Initial state
    record = InspectionRecord(
        inspection_id=inspection_id,
        image_path=str(file_path),
        status=None
    )
    MOCK_DB[inspection_id] = record
    return record

@router.post("/{inspection_id}/process", response_model=InspectionRecord)
async def process_inspection(inspection_id: str):
    record = MOCK_DB.get(inspection_id)
    if not record:
        return {"error": "Inspection not found"}
        
    # Run LangGraph pipeline
    initial_state = {"inspection_id": inspection_id, "image_path": record.image_path}
    final_state = inspection_app.invoke(initial_state)
    
    # Update record with graph results
    record.marker_detected = final_state.get("marker_detected", False)
    record.homography = final_state.get("homography")
    record.detections = final_state.get("detections", [])
    record.ocr_results = final_state.get("ocr_results", [])
    record.product_data = final_state.get("product_data")
    record.rule_results = final_state.get("rule_results", [])
    record.score = final_state.get("score", 0)
    record.status = final_state.get("status")
    
    MOCK_DB[inspection_id] = record
    return record

@router.get("/{inspection_id}", response_model=InspectionRecord)
async def get_inspection(inspection_id: str):
    return MOCK_DB.get(inspection_id)