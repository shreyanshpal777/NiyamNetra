from langgraph.graph import StateGraph, END
from app.pipeline.state import InspectionState
from app.vision.pipeline import process_image
from app.llm.client import extract_product_data
from app.compliance.engine import compliance_engine


def process_vision(state: InspectionState) -> dict:
    image_path = state.get("image_path")
    if not image_path:
        return {}

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    result = process_image(image_bytes)
    return {
        "marker_detected": result.get("marker_detected", False),
        "marker_corners": result.get("marker_corners"),
        "homography": result.get("homography"),
        "ocr_results": result.get("ocr_results", []),
        "measurements": result.get("measurements", {}),
        "annotated_image": result.get("annotated_image"),
    }


def extract_semantics(state: InspectionState) -> dict:
    ocr_results = state.get("ocr_results", [])
    product_data = extract_product_data(ocr_results)
    return {"product_data": product_data}


def evaluate_rules(state: InspectionState) -> dict:
    product_data = state.get("product_data")
    ocr_results = state.get("ocr_results", [])
    results, score, status = compliance_engine.evaluate(product_data, ocr_results)
    return {
        "rule_results": results,
        "score": score,
        "status": status,
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