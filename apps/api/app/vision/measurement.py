"""
Converts pixel-space OCR bounding boxes into physical (mm) measurements
using the homography / scale computed from the ArUco marker, and builds
the resulting OCRWord objects + a measurements summary.
"""
from __future__ import annotations

import cv2
import numpy as np

from app.models.ocr import OCRWord


def _bbox_height_px(bbox: list[list[float]]) -> float:
    """Average of the two vertical (left/right) side lengths of a
    4-point polygon bbox in TL, TR, BR, BL order."""
    pts = np.array(bbox, dtype=np.float64)
    left_side = np.linalg.norm(pts[0] - pts[3])
    right_side = np.linalg.norm(pts[1] - pts[2])
    return float((left_side + right_side) / 2.0)


def _bbox_height_mm_via_homography(
    bbox: list[list[float]], homography: list[list[float]]
) -> float:
    h_matrix = np.array(homography, dtype=np.float64)
    pts = np.array(bbox, dtype=np.float64).reshape(-1, 1, 2)
    mm_pts = cv2.perspectiveTransform(pts, h_matrix).reshape(-1, 2)
    left_side = np.linalg.norm(mm_pts[0] - mm_pts[3])
    right_side = np.linalg.norm(mm_pts[1] - mm_pts[2])
    return float((left_side + right_side) / 2.0)


def apply_measurements(
    ocr_words: list[dict],
    homography: list[list[float]] | None,
    px_per_mm: float | None,
) -> tuple[list[OCRWord], dict]:
    """
    Fills in height_px / height_mm for each OCR word and builds a summary
    measurements dict.

    ocr_words: list of dicts with "text", "confidence", "bbox" (as
    returned by ocr.run_ocr).

    Returns (list[OCRWord], measurements_dict).
    """
    enriched: list[OCRWord] = []
    heights_mm: list[float] = []

    for word in ocr_words:
        bbox = word["bbox"]
        height_px = _bbox_height_px(bbox)

        height_mm = None
        if homography is not None:
            try:
                height_mm = _bbox_height_mm_via_homography(bbox, homography)
            except cv2.error:
                height_mm = None
        if height_mm is None and px_per_mm:
            height_mm = height_px / px_per_mm

        if height_mm is not None:
            heights_mm.append(height_mm)

        enriched.append(
            OCRWord(
                text=word["text"],
                confidence=word["confidence"],
                bbox=bbox,
                height_px=height_px,
                height_mm=height_mm,
            )
        )

    measurements = {
        "px_per_mm": px_per_mm,
        "scale_method": "homography" if homography is not None else ("px_per_mm" if px_per_mm else None),
        "num_ocr_words": len(enriched),
        "min_text_height_mm": min(heights_mm) if heights_mm else None,
        "max_text_height_mm": max(heights_mm) if heights_mm else None,
        "avg_text_height_mm": (sum(heights_mm) / len(heights_mm)) if heights_mm else None,
    }
    return enriched, measurements
