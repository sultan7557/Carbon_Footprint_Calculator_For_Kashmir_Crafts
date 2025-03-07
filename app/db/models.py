from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    main_category = Column(String, nullable=True)
    subcategory = Column(String, nullable=True)
    craft_category = Column(String, nullable=True)
    craft_type = Column(String, nullable=True)
    raw_material = Column(String, nullable=True)
    processing = Column(String, nullable=True)
    crafting = Column(String, nullable=True)
    shipping_distance = Column(Float, nullable=True)
    fabric_choice = Column(String, nullable=True)
    shipping_volume = Column(String, nullable=True)
    shipping_location = Column(String, nullable=True)
    dkc_warehouse = Column(String, nullable=True)
    packaging = Column(String, nullable=True)
    transportation = Column(String, nullable=True)
    quality = Column(String, nullable=True)
    ply_type = Column(String, nullable=True)
    weaving_design = Column(String, nullable=True)
    certifications = Column(String, nullable=True)
    embellishments = Column(String, nullable=True)
    product_line_size = Column(String, nullable=True)
    carbon_footprint = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())