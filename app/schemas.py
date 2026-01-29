from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VehicleBase(BaseModel):
    # manufacturer_name: Optional[str] = None
    manufacturer_name: str
    horse_power: int
    model_name: str
    model_year: int
    purchase_price: float
    fuel_type: str
    description: str

class VehicleCreate(VehicleBase):
    vin: str

class VehicleOut(VehicleBase):
    vin: str
    last_updated: datetime

    class Config:
        # orm_mode = True
        from_attributes = True
