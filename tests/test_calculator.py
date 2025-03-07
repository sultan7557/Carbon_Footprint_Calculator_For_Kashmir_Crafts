import pytest
from app.services.calculator import CarbonFootprintCalculator
from app.models.schemas import PashminaInput

def test_calculator_initialization():
    calculator = CarbonFootprintCalculator()
    assert calculator.model is not None
    assert calculator.label_encoders is not None

def test_prediction_with_complete_data():
    calculator = CarbonFootprintCalculator()
    input_data = PashminaInput(
        material_type="Ultra-Fine Pashmina",
        production_process="Hand Spinning, Hand Weaving",
        dye_type="Natural-Dyed",
        shipping_distance=1000
    )
    result = calculator.predict_carbon_footprint(input_data)
    assert isinstance(result["carbon_footprint"], float)
    assert result["confidence_level"] == "high"

def test_prediction_with_partial_data():
    calculator = CarbonFootprintCalculator()
    input_data = PashminaInput(
        material_type="Ultra-Fine Pashmina",
        shipping_distance=1000
    )
    result = calculator.predict_carbon_footprint(input_data)
    assert isinstance(result["carbon_footprint"], float)
    assert result["confidence_level"] == "medium"