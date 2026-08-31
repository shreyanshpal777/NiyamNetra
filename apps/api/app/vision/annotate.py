"""
Draws ArUco + OCR bounding boxes on the captured image for the demo UI's
"View Annotated Image" screen.
"""
from __future__ import annotations

import cv2
import numpy as np

from app.models.ocr import OCRWord

MARKER_COLOR = (0, 200, 0)   # green, BGR
OCR_COLOR = (255, 140, 0)    # orange-blue, BGR
TEXT_COLOR = (255, 255, 255)


def draw_annotations(
    image: np.ndarray,
    marker_corners: list[list[float]] | None,
    marker_id: int | None,
    ocr_words: list[OCRWord],
) -> np.ndarray:
    """Returns a new annotated BGR image; does not mutate the input."""
    annotated = image.copy()

    if marker_corners is not None:
        pts = np.array(marker_corners, dtype=np.int32).reshape(-1, 1, 2)
        cv2.polylines(annotated, [pts], isClosed=True, color=MARKER_COLOR, thickness=3)
        label = f"ArUco {marker_id}" if marker_id is not None else "ArUco"
        _draw_label(annotated, label, tuple(pts[0][0]), MARKER_COLOR)

    for word in ocr_words:
        pts = np.array(word.bbox, dtype=np.int32).reshape(-1, 1, 2)
        cv2.polylines(annotated, [pts], isClosed=True, color=OCR_COLOR, thickness=2)
        label = f"{word.text} ({word.confidence * 100:.0f}%)"
        _draw_label(annotated, label, tuple(pts[0][0]), OCR_COLOR)

    return annotated


def _draw_label(image: np.ndarray, text: str, origin: tuple[int, int], box_color: tuple[int, int, int]) -> None:
    x, y = origin
    y = max(y - 8, 12)
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.5
    thickness = 1
    (tw, th), _ = cv2.getTextSize(text, font, scale, thickness)
    cv2.rectangle(image, (x, y - th - 4), (x + tw + 4, y + 2), box_color, -1)
    cv2.putText(image, text, (x + 2, y - 2), font, scale, TEXT_COLOR, thickness, cv2.LINE_AA)
