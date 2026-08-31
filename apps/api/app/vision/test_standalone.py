"""
Standalone test — run this directly to validate the pipeline against a
real photo before it's wired into FastAPI.

Usage:
    python test_standalone.py path/to/photo.jpg

Prints the detection/OCR/measurement summary as JSON and writes
annotated_output.jpg next to the input image.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2

# Allow running this file directly from the vision/ folder during testing,
# without needing the full `app.` package layout in place yet.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.vision.pipeline import process_image  # noqa: E402


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python test_standalone.py path/to/photo.jpg")
        sys.exit(1)

    image_path = Path(sys.argv[1])
    image_bytes = image_path.read_bytes()

    result = process_image(image_bytes)

    annotated = result.pop("annotated_image")
    out_path = image_path.parent / "annotated_output.jpg"
    cv2.imwrite(str(out_path), annotated)

    printable = {
        "marker_detected": result["marker_detected"],
        "marker_corners": result["marker_corners"],
        "measurements": result["measurements"],
        "ocr_results": [w.model_dump() for w in result["ocr_results"]],
    }
    print(json.dumps(printable, indent=2))
    print(f"\nAnnotated image written to: {out_path}")


if __name__ == "__main__":
    main()
