from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models.schemas import PashminaInput, CarbonFootprintResponse
from app.services.calculator import CarbonFootprintCalculator
from app.db.database import engine, get_db, SessionLocal
from app.db import models
from app.db.crud import create_calculation

app = FastAPI(
    title="Carbon Footprint Calculator API",
    description="API for calculating carbon footprint of Pashmina products",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

# Templates
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

calculator = CarbonFootprintCalculator()

# Create database tables on startup
@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("calculator.html", {"request": request})


@app.post("/calculate-carbon-footprint", response_model=CarbonFootprintResponse)
async def calculate_carbon_footprint(input_data: PashminaInput, db: SessionLocal = Depends(get_db)):
    try:
        result = calculator.predict_carbon_footprint(input_data)

        resolved_inputs = {
            "main_category": input_data.main_category,
            "subcategory": input_data.subcategory,
            "craft_category": input_data.craft_category,
            "craft_type": input_data.craft_type,
            "raw_material": input_data.raw_material,
            "processing": input_data.processing,
            "crafting": input_data.crafting,
            "shipping_distance": float(input_data.shipping_distance) if input_data.shipping_distance and input_data.shipping_distance != "I don’t know" else 1000,
            "shipping_volume": input_data.shipping_volume,
            "shipping_location": input_data.shipping_location,
            "dkc_warehouse": input_data.dkc_warehouse if input_data.shipping_location == "DKC" else None,
            "packaging": input_data.packaging,
            "transportation": input_data.transportation,
            "quality": input_data.quality,
            "ply_type": input_data.ply_type,
            "weaving_design": input_data.weaving_design,
            "certifications": input_data.certifications,
            "embellishments": input_data.embellishments,
            "product_line_size": input_data.product_line_size,
            "carbon_footprint": result["carbon_footprint"]
        }

        try:
            create_calculation(db, resolved_inputs)
        except Exception as db_error:
            print(f"Database error: {db_error}")

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}