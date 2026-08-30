from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "inspector_ai"
    groq_api_key: str = ""
    llm_model: str = "llama-3.1-8b-instant"
    yolo_model: str = ""
    ocr_language: str = "en"
    aruco_marker_size_mm: float = 50.0
    upload_dir: Path = Path("data/uploads")
    report_dir: Path = Path("data/reports")
    device: str = "cpu"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    settings.report_dir.mkdir(parents=True, exist_ok=True)
    return settings
