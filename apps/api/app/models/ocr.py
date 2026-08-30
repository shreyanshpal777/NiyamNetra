from pydantic import BaseModel, Field


class OCRWord(BaseModel):
    text: str
    confidence: float = Field(ge=0, le=1)
    bbox: list[list[float]]
    height_px: float = Field(ge=0)
    height_mm: float | None = None
