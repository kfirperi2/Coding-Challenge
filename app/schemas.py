from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VehicleBase(BaseModel):
    manufacturer_name: Optional[str] = None
    horse_power: Optional[int] = None
    purchase_price: Optional[float] = None
    fuel_type: Optional[str] = None
    description: Optional[str] = None

class VehicleCreate(VehicleBase):
    vin: str

class VehicleOut(VehicleBase):
    vin: str
    last_updated: datetime

class Config:
    orm_mode = True
