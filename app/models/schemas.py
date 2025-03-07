from typing import Optional
from pydantic import BaseModel, Field

class PashminaInput(BaseModel):
    main_category: Optional[str] = Field(None, description="Main category from frontend", example="Interior Decor")
    subcategory: Optional[str] = Field(None, description="Subcategory from frontend", example="Papier-Mâché Items")
    craft_category: Optional[str] = Field(None, description="Category of craft", example="Interior Decor")
    craft_type: Optional[str] = Field(None, description="Type of craft", example="Papier-Mâché Items")
    raw_material: Optional[str] = Field(None, description="Raw material used", example="Waste Paper and Cotton Rags")
    embedded_material: Optional[str] = Field(None, description="Embedded material (for Papier-Mâché)", example="Wood")
    processing: Optional[str] = Field(None, description="Processing method", example="Traditional Paper Mâché Method")
    crafting: Optional[str] = Field(None, description="Crafting method", example="Natural-Dyed")
    certifications: Optional[str] = Field(None, description="Applicable certifications", example="GOTS")
    weaving_design: Optional[str] = Field(None, description="Weaving/design", example="Plain Weave")
    finishing_technique: Optional[str] = Field(None, description="Finishing technique", example="Hand-Painted")
    shipping_distance: Optional[str] = Field(None, description="Shipping distance in kilometers or 'I don’t know'", example="1000")
    shipping_volume: Optional[str] = Field(None, description="Volume of shipping", example="Individual")
    shipping_location: Optional[str] = Field(None, description="Shipping location (e.g., Kashmir or DKC)", example="Kashmir")
    dkc_warehouse: Optional[str] = Field(None, description="DKC warehouse location if applicable", example="West Coast")
    packaging: Optional[str] = Field(None, description="Type of packaging", example="Eco-friendly Packaging Materials")
    transportation: Optional[str] = Field(None, description="Mode of transportation", example="Sea")
    quality: Optional[str] = Field(None, description="Quality or blend type", example="Pure Pashmina")
    ply_type: Optional[str] = Field(None, description="Ply type (e.g., Single-Ply)", example="Single-Ply")
    embellishments: Optional[str] = Field(None, description="Any embellishments used", example="Full Dense Embroidery")
    product_line_size: Optional[str] = Field(None, description="Product line & standard size", example="Shawls (80\"x40\")")

class CarbonFootprintResponse(BaseModel):
    carbon_footprint: float = Field(..., description="Calculated carbon footprint in kg CO2e")
    unit: str = Field(..., description="Unit of measurement")
    confidence_level: str = Field(..., description="Confidence level of the prediction")
    recommendations: list[str] = Field(..., description="List of recommendations for reduction")
    explanations: list[str] = Field(..., description="List of explanations for assumptions made")
    breakdown: dict = Field(..., description="Detailed breakdown of emissions")