"""
OCR extraction using PaddleOCR.

Loads the OCR engine once (lazy singleton, since model load is slow) and
exposes run_ocr(), which returns text + confidence + pixel bounding boxes
for every detected text region. Physical (mm) measurement is applied
separately in measurement.py once ArUco calibration is available.
"""
from __future__ import annotations

import numpy as np

_ocr_engine = None


def _get_engine():
    global _ocr_engine
    if _ocr_engine is None:
        from paddleocr import PaddleOCR

        _ocr_engine = PaddleOCR(use_angle_cls=True, lang="en", show_log=False)
    return _ocr_engine


def run_ocr(image: np.ndarray, min_confidence: float = 0.4) -> list[dict]:
    """
    Run OCR on a BGR numpy image.

    Returns a list of dicts:
        {
            "text": str,
            "confidence": float,          # 0-1
            "bbox": list[list[float]],    # 4 (x, y) points, TL,TR,BR,BL
        }
    """
    engine = _get_engine()
    raw_result = engine.ocr(image, cls=True)

    if not raw_result or raw_result[0] is None:
        return []

    words = []
    for line in raw_result[0]:
        bbox, (text, confidence) = line
        if confidence < min_confidence:
            continue
        words.append(
            {
                "text": text,
                "confidence": float(confidence),
                "bbox": [[float(x), float(y)] for x, y in bbox],
            }
        )
    return words
