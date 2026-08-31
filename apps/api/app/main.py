from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import inspections
from app.core.logging import configure_logging
from app.database import connect_to_mongo, close_mongo_connection, get_db
from app.database import create_inspection, InspectionDocument

configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(title="Inspector AI", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    try:
        db = get_db()
        await db.command("ping")
        return {"status": "ok", "mongodb": "connected"}
    except Exception as e:
        return {"status": "error", "mongodb": str(e)}


@app.post("/seed")
async def seed_demo():
    doc = InspectionDocument(
        id="INS-001",
        product_name="Premium Wheat Flour",
        category="Staple food",
        status="COMPLETED",
        score=96,
        image_path="/uploads/INS-001.png",
        extracted_data=None,
        ocr_words=[],
        rule_results=[],
    )
    result = await create_inspection(doc)
    return {"message": "Demo inspection created", "inspection_id": result.id}


app.include_router(inspections.router, prefix="/api/inspections", tags=["Inspections"])
