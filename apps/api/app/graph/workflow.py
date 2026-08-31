from langgraph.graph import StateGraph, END
from app.graph.state import InspectionState
from app.vision.pipeline import detect_aruco, calculate_homography, pixel_to_mm, YOLODetector, OCRService
from app.llm.core import extract_product_data
from app.compliance.engine import evaluate_compliance

# Initialize services
yolo = YOLODetector()
ocr = OCRService()

def process_vision(state: InspectionState) -> dict:
    image_path = state["image_path"]
    
    # 1. Calibration
    marker_detected, corners = detect_aruco(image_path)
    homography = calculate_homography(corners) if marker_detected else None
    
    # 2. YOLO & OCR
    detections = yolo.detect_label(image_path)
    ocr_results = ocr.run_ocr(image_path)
    
    # 3. Measurement mapping
    for word in ocr_results:
        word.height_mm = pixel_to_mm(word.height_px, homography)
        
    return {
        "marker_detected": marker_detected,
        "marker_corners": corners,
        "homography": homography,
        "detections": detections,
        "ocr_results": ocr_results
    }

def extract_semantics(state: InspectionState) -> dict:
    product_data = extract_product_data(state["ocr_results"])
    return {"product_data": product_data}

def evaluate_rules(state: InspectionState) -> dict:
    results, score, status = evaluate_compliance(state["product_data"], state["ocr_results"])
    return {
        "rule_results": results,
        "score": score,
        "status": status
    }

# Build the Graph
workflow = StateGraph(InspectionState)
workflow.add_node("vision", process_vision)
workflow.add_node("semantics", extract_semantics)
workflow.add_node("compliance", evaluate_rules)

workflow.set_entry_point("vision")
workflow.add_edge("vision", "semantics")
workflow.add_edge("semantics", "compliance")
workflow.add_edge("compliance", END)

inspection_app = workflow.compile()