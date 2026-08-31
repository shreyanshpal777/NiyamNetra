from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import inspections
from app.core.config import configure_logging

configure_logging()

app = FastAPI(title="Inspector AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inspections.router, prefix="/api/inspections", tags=["Inspections"])