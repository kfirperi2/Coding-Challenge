from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from sqlalchemy.dialects.postgresql import CITEXT

class Manufacturer(Base):
    __tablename__ = "manufacturer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=True)
    factory_location = Column(String, nullable=True)

    # Relationship to Model
    models = relationship("Model", back_populates="manufacturer", cascade="all, delete-orphan")

class Model(Base):
    __tablename__ = "model"

    id = Column(String(100), primary_key=True)
    name = Column(String, nullable=False)
    trim = Column(String, nullable=True)
    manufacturer_id = Column(Integer, ForeignKey("manufacturer.id"), nullable=False)
    horsepower = Column(Integer, nullable=True)

    # Relationship to Manufacturer
    manufacturer = relationship("Manufacturer", back_populates="models")

    # Relationship to Vehicle
    vehicles = relationship("Vehicle", back_populates="model", cascade="all, delete-orphan")

class Fuel(Base):
    __tablename__ = "fuel"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)

    # Relationship to Vehicle
    vehicles = relationship("Vehicle", back_populates="fuel")

class Vehicle(Base):
    __tablename__ = "vehicle"
    
    vin = Column(CITEXT, primary_key=True)
    model_id = Column(String, ForeignKey("model.id"), nullable=False)
    fuel_id = Column(Integer, ForeignKey("fuel.id"), nullable =False)
    model_year = Column(Integer, nullable=False)
    purchase_price = Column(Numeric(12,2))
    description = Column(Text, nullable=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    model = relationship("Model", back_populates="vehicles")
    fuel = relationship("Fuel", back_populates="vehicles")
