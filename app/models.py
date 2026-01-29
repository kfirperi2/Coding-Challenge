from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from .database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"
    
    vin = Column(String, primary_key=True)
    manufacturer_name = Column(String, nullable=False)
    horse_power = Column(Integer, nullable=False)
    model_name = Column(String, nullable=False)
    model_year = Column(Integer, nullable=False)
    purchase_price = Column(Numeric(12,2), nullable=False)
    fuel_type = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
