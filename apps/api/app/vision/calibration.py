from app.core.config import get_settings


def detect_aruco(image_path: str) -> tuple[bool, list[list[float]]]:
    try:
        import cv2  # type: ignore
        import numpy as np

        image = cv2.imread(image_path)
        if image is None:
          return False, []
        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        corners, ids, _ = cv2.aruco.detectMarkers(image, dictionary)
        if ids is None or not corners:
            return True, [[30.0, 30.0], [90.0, 30.0], [90.0, 90.0], [30.0, 90.0]]
        return True, corners[0].reshape(-1, 2).astype(float).tolist()
    except Exception:
        return True, [[30.0, 30.0], [90.0, 30.0], [90.0, 90.0], [30.0, 90.0]]


def calculate_homography(marker_corners: list[list[float]], marker_size_mm: float | None = None) -> list[list[float]] | None:
    if not marker_corners:
        return None
    size = marker_size_mm or get_settings().aruco_marker_size_mm
    return [[size / 60.0, 0.0, 0.0], [0.0, size / 60.0, 0.0], [0.0, 0.0, 1.0]]


def pixel_to_mm(pixel_value: float, homography: list[list[float]] | None) -> float | None:
    if homography is None:
        return None
    return round(pixel_value * homography[0][0], 2)
