import cv2
import numpy as np
from app.core.config import get_settings


def detect_aruco(image_path: str) -> tuple[bool, list[list[float]]]:
    image = cv2.imread(image_path)
    if image is None:
        return False, []
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    try:
        # OpenCV 4.7+ API
        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(dictionary, parameters)
        corners, ids, _ = detector.detectMarkers(gray)
    except AttributeError:
        # Fallback for older OpenCV versions
        dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
        parameters = cv2.aruco.DetectorParameters_create()
        corners, ids, _ = cv2.aruco.detectMarkers(gray, dictionary, parameters=parameters)
        
    if ids is not None and len(corners) > 0:
        # Return the corners of the first detected marker (top-left, top-right, bottom-right, bottom-left)
        return True, corners[0].reshape(-1, 2).astype(float).tolist()
        
    return False, []


def calculate_homography(marker_corners: list[list[float]], marker_size_mm: float | None = None) -> list[list[float]] | None:
    if not marker_corners or len(marker_corners) != 4:
        return None
        
    size = marker_size_mm or get_settings().aruco_marker_size_mm
    
    src_pts = np.array(marker_corners, dtype=np.float32)
    dst_pts = np.array([
        [0, 0],
        [size, 0],
        [size, size],
        [0, size]
    ], dtype=np.float32)
    
    matrix, _ = cv2.findHomography(src_pts, dst_pts)
    
    if matrix is not None:
        return matrix.tolist()
    return None


def pixel_to_mm(pixel_value: float, homography: list[list[float]] | None) -> float | None:
    if homography is None:
        return None
        
    H = np.array(homography)
    
    # Extract approximate linear scale factors from the perspective matrix
    scale_x = np.sqrt(H[0, 0]**2 + H[0, 1]**2)
    scale_y = np.sqrt(H[1, 0]**2 + H[1, 1]**2)
    
    # Average the X and Y scales for a 1D scalar (assuming roughly square aspect)
    avg_scale = (scale_x + scale_y) / 2.0
    
    return round(pixel_value * float(avg_scale), 2)
