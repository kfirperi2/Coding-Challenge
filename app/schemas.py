from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VehicleBase(BaseModel):
    model_id: str
    fuel_id: int
    model_year: int
    purchase_price: Optional[float] = None
    description: Optional[str] = None

class VehicleCreate(VehicleBase):
    vin: str

class VehicleOut(VehicleBase):
    vin: str
    last_update: datetime

class Config:
    orm_mode = True
