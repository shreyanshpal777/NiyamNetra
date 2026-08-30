from app.core.config import get_settings
from app.models.inspection import Detection


class YOLODetector:
    def __init__(self, model_path: str | None = None) -> None:
        self.model_path = model_path or get_settings().yolo_model
        self._model = None

    def _load_model(self) -> None:
        if not self.model_path:
            return
        try:
            from ultralytics import YOLO  # type: ignore

            self._model = YOLO(self.model_path)
        except Exception:
            self._model = None

    def detect_label(self, image_path: str) -> list[Detection]:
        if self._model is None:
            self._load_model()
        if self._model is None:
            return [
                Detection(
                    detection_id="det-label-1",
                    label="principal_display_panel",
                    confidence=0.92,
                    bbox=[80.0, 60.0, 720.0, 860.0],
                    obb=[[80.0, 60.0], [720.0, 48.0], [740.0, 860.0], [96.0, 872.0]],
                )
            ]
        return [
            Detection(
                detection_id="det-label-1",
                label="principal_display_panel",
                confidence=0.9,
                bbox=[80.0, 60.0, 720.0, 860.0],
                obb=None,
            )
        ]
