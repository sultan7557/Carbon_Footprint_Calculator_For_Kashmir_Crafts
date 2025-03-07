from sqlalchemy.orm import Session
from .models import Calculation

def create_calculation(db: Session, calculation_data: dict):
    db_calculation = Calculation(**calculation_data)
    db.add(db_calculation)
    db.commit()
    db.refresh(db_calculation)
    return db_calculation