"""
Dynamic OCR extraction using EasyOCR & PaddleOCR.
"""
from __future__ import annotations

import os
import logging
import numpy as np

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

_ocr_reader = None
_ocr_backend = None


def _get_reader():
    global _ocr_reader, _ocr_backend
    if _ocr_reader is not None:
        return _ocr_reader, _ocr_backend

    try:
        import easyocr
        _ocr_reader = easyocr.Reader(["en"], gpu=False, verbose=False)
        _ocr_backend = "easyocr"
        logging.info("Initialized EasyOCR engine successfully.")
        return _ocr_reader, _ocr_backend
    except Exception as e:
        logging.warning(f"EasyOCR init failed: {e}")

    try:
        from paddleocr import PaddleOCR
        _ocr_reader = PaddleOCR(use_angle_cls=True, lang="en", show_log=False)
        _ocr_backend = "paddleocr"
        logging.info("Initialized PaddleOCR engine successfully.")
        return _ocr_reader, _ocr_backend
    except Exception as e:
        logging.warning(f"PaddleOCR init failed: {e}")

    return None, None


def run_ocr(image: np.ndarray, min_confidence: float = 0.1) -> list[dict]:
    """
    Run dynamic OCR on a BGR numpy image.

    Returns a list of dicts:
        {
            "text": str,
            "confidence": float,          # 0-1
            "bbox": list[list[float]],    # 4 (x, y) points, TL,TR,BR,BL
        }
    """
    import cv2
    reader, backend = _get_reader()
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) if image.ndim == 3 else image

    if backend == "easyocr" and reader is not None:
        try:
            results = reader.readtext(rgb)
            words = []
            for bbox, text, prob in results:
                if prob < min_confidence or not text.strip():
                    continue
                pts = [[float(p[0]), float(p[1])] for p in bbox]
                words.append({
                    "text": text.strip(),
                    "confidence": float(prob),
                    "bbox": pts,
                })
            if words:
                return words
        except Exception as e:
            logging.error(f"EasyOCR execution error: {e}")

    if backend == "paddleocr" and reader is not None:
        try:
            raw_result = reader.ocr(image, cls=True)
            if raw_result and raw_result[0]:
                words = []
                for line in raw_result[0]:
                    bbox, (text, confidence) = line
                    if confidence < min_confidence or not text.strip():
                        continue
                    words.append({
                        "text": text.strip(),
                        "confidence": float(confidence),
                        "bbox": [[float(x), float(y)] for x, y in bbox],
                    })
                if words:
                    return words
        except Exception as e:
            logging.error(f"PaddleOCR execution error: {e}")

    return []



