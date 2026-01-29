from pydantic import BaseModel, field_validator, Field
from datetime import datetime

ALLOWED_FUEL_TYPES = {"Gasoline Regular", "Gasoline Mid-Grade", "Gasoline Premium", "Diesel"}

class VehicleBase(BaseModel):
    manufacturer_name: str
    horse_power: int
    model_name: str
    model_year: int
    purchase_price: float
    fuel_type: str
    description: str

    @field_validator("manufacturer_name", "model_name", "fuel_type", mode="before")
    @classmethod
    def strip_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v
    
    @field_validator("horse_power")
    @classmethod
    def horse_power_positive(cls, v):
        if v <= 0:
            raise ValueError("horse_power must be greater than 0")
        return v

    @field_validator("purchase_price")
    @classmethod
    def price_positive(cls, v):
        if v < 0:
            raise ValueError("purchase_price must be non-negative")
        return v
    
    @field_validator("model_year")
    @classmethod
    def validate_year(cls, v):
        if v is None or v > datetime.now().year:
            raise ValueError("model_year cannot be in the future")
        return v

    @field_validator("fuel_type")
    @classmethod
    def validate_fuel_type(cls, v):
        if v not in ALLOWED_FUEL_TYPES:
            raise ValueError(f"fuel_type must be one of {ALLOWED_FUEL_TYPES}")
        return v.lower()

class VehicleCreate(VehicleBase):
    vin: str = Field(..., max_length=17, description="Vehicle VIN")

class VehicleOut(BaseModel):
    vin: str  
    manufacturer_name: str
    horse_power: int
    model_name: str
    model_year: int
    purchase_price: float
    fuel_type: str
    description: str
    last_updated: datetime

    class Config:
        from_attributes = True

    @field_validator("manufacturer_name", "model_name", "fuel_type", mode="before")
    @classmethod
    def strip_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v
    
    @field_validator("horse_power")
    @classmethod
    def horse_power_positive(cls, v):
        if v <= 0:
            raise ValueError("horse_power must be greater than 0")
        return v

    @field_validator("purchase_price")
    @classmethod
    def price_positive(cls, v):
        if v < 0:
            raise ValueError("purchase_price must be non-negative")
        return v