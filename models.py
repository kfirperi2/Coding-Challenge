from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Vehicle(Base):
    __tablename__ = "vehicle"

    vin = Column(String(17), primary_key=True)
    model_id = Column(String, ForeignKey("model.id"), nullable=False)
    fuel_id = Column(Integer, ForeignKey("fuel.id"), nullable =False)
    model_year = Column(Integer, nullable=False)
    purchase_price = Column(Numeric(12,2))
    description = Column(String)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    model = relationship("Model")
    fuel = relationship("Fuel")
