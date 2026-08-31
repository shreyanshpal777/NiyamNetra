"""
Top-level entrypoint for the vision module.

Runs: ArUco calibration -> OCR -> physical measurement -> annotation,
and returns a dict whose keys line up with app.pipeline.state.InspectionState
so the API/pipeline layer can merge it directly into an InspectionRecord.

Usage (from wherever POST /api/inspect is handled):

    from app.vision.pipeline import process_image

    result = process_image(image_bytes)
    # result["marker_detected"], result["ocr_results"], etc.
"""
from __future__ import annotations

import cv2
import numpy as np

from app.vision.annotate import draw_annotations
from app.vision.aruco import (
    DEFAULT_MARKER_ID,
    DEFAULT_MARKER_SIZE_MM,
    compute_scale_and_homography,
    detect_aruco_marker,
)
from app.vision.measurement import apply_measurements
from app.vision.ocr import run_ocr


def process_image(
    image_bytes: bytes,
    marker_id: int = DEFAULT_MARKER_ID,
    marker_size_mm: float = DEFAULT_MARKER_SIZE_MM,
) -> dict:
    """
    Runs the full vision pipeline on raw image bytes (e.g. an uploaded jpg/png).

    Returns:
        {
            "marker_detected": bool,
            "marker_corners": list[list[float]] | None,
            "homography": list[list[float]] | None,
            "ocr_results": list[OCRWord],
            "measurements": dict[str, float | str | None],
            "annotated_image": np.ndarray,  # BGR, for saving/serving to the frontend
        }

    Raises ValueError if the image bytes can't be decoded.
    """
    np_arr = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Could not decode image bytes")

    marker_result = detect_aruco_marker(image, marker_id=marker_id)

    homography = None
    px_per_mm = None
    if marker_result["marker_detected"]:
        scale_result = compute_scale_and_homography(
            marker_result["marker_corners"], marker_size_mm=marker_size_mm
        )
        homography = scale_result["homography"]
        px_per_mm = scale_result["px_per_mm"]

    raw_ocr_words = run_ocr(image)
    ocr_results, measurements = apply_measurements(raw_ocr_words, homography, px_per_mm)

    annotated_image = draw_annotations(
        image,
        marker_result["marker_corners"],
        marker_result["marker_id"],
        ocr_results,
    )

    return {
        "marker_detected": marker_result["marker_detected"],
        "marker_corners": marker_result["marker_corners"],
        "homography": homography,
        "ocr_results": ocr_results,
        "measurements": measurements,
        "annotated_image": annotated_image,
    }
