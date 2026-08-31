"""
ArUco marker detection and pixel-to-mm calibration.

A single printed ArUco marker (default: DICT_4X4_50, ID=23, 50x50mm) is
placed next to the product label as a physical scale + perspective
reference. This module finds the marker in the captured image and turns
its known physical size into:

  - a simple px_per_mm scale factor (quick, assumes fronto-parallel shot)
  - a full homography mapping pixel coords -> mm coords on the label plane
    (assumes the label is coplanar with the marker, which corrects for
    mild perspective/tilt)
"""
from __future__ import annotations

import cv2
import numpy as np

DEFAULT_DICT = cv2.aruco.DICT_4X4_50
DEFAULT_MARKER_ID = 23
DEFAULT_MARKER_SIZE_MM = 50.0


def _get_detector(dictionary_id: int = DEFAULT_DICT):
    """Supports both the new (OpenCV >=4.7) and legacy cv2.aruco APIs."""
    aruco_dict = cv2.aruco.getPredefinedDictionary(dictionary_id)
    if hasattr(cv2.aruco, "ArucoDetector"):
        params = cv2.aruco.DetectorParameters()
        return cv2.aruco.ArucoDetector(aruco_dict, params), "new"
    params = cv2.aruco.DetectorParameters_create()
    return (aruco_dict, params), "legacy"


def detect_aruco_marker(
    image: np.ndarray,
    marker_id: int = DEFAULT_MARKER_ID,
    dictionary_id: int = DEFAULT_DICT,
) -> dict:
    """
    Detect the reference ArUco marker in a BGR image.

    Returns:
        {
            "marker_detected": bool,
            "marker_id": int | None,
            "marker_corners": list[list[float]] | None,  # TL,TR,BR,BL pixel points
            "all_detected_ids": list[int],
        }
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image

    detector, mode = _get_detector(dictionary_id)
    if mode == "new":
        corners, ids, _ = detector.detectMarkers(gray)
    else:
        aruco_dict, params = detector
        corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=params)

    result = {
        "marker_detected": False,
        "marker_id": None,
        "marker_corners": None,
        "all_detected_ids": [],
    }

    if ids is None or len(ids) == 0:
        return result

    ids_flat = ids.flatten().tolist()
    result["all_detected_ids"] = ids_flat

    if marker_id not in ids_flat:
        return result

    idx = ids_flat.index(marker_id)
    marker_corners = corners[idx].reshape(4, 2).tolist()  # TL, TR, BR, BL

    result["marker_detected"] = True
    result["marker_id"] = marker_id
    result["marker_corners"] = marker_corners
    return result


def compute_scale_and_homography(
    marker_corners: list[list[float]],
    marker_size_mm: float = DEFAULT_MARKER_SIZE_MM,
) -> dict:
    """
    Given the 4 pixel corners of the marker (TL, TR, BR, BL order, as
    returned by detect_aruco_marker), compute the scale and homography.

    Returns:
        {
            "px_per_mm": float | None,
            "avg_marker_side_px": float,
            "homography": list[list[float]] | None,  # 3x3, pixel -> mm
        }
    """
    src = np.array(marker_corners, dtype=np.float32)

    side_lengths = [
        np.linalg.norm(src[0] - src[1]),
        np.linalg.norm(src[1] - src[2]),
        np.linalg.norm(src[2] - src[3]),
        np.linalg.norm(src[3] - src[0]),
    ]
    avg_side_px = float(np.mean(side_lengths))
    px_per_mm = avg_side_px / marker_size_mm if marker_size_mm > 0 else None

    dst = np.array(
        [
            [0, 0],
            [marker_size_mm, 0],
            [marker_size_mm, marker_size_mm],
            [0, marker_size_mm],
        ],
        dtype=np.float32,
    )

    homography = None
    try:
        h_matrix, _ = cv2.findHomography(src, dst, method=0)
        if h_matrix is not None:
            homography = h_matrix.tolist()
    except cv2.error:
        homography = None

    return {
        "px_per_mm": px_per_mm,
        "avg_marker_side_px": avg_side_px,
        "homography": homography,
    }
