from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models
from . import schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vehicle APIs")

@app.get("/vehicle", response_model=list[schemas.VehicleOut])
def get_vehicles(db: Session = Depends(get_db)):
    try:
        vehicles = db.query(models.Vehicle).all()
        return vehicles
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/vehicle/{vin}", response_model=schemas.VehicleOut)
def get_vehicle(vin: str, db: Session = Depends(get_db)):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.vin == vin).first()
    if not vehicle:
        raise HTTPException(status_code=400, detail="Vehicle not found")
    return vehicle

@app.post("/vehicle", response_model=schemas.VehicleOut, status_code=201)
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    db_vehicle = db.query(models.Vehicle).filter(models.Vehicle.vin == vehicle.vin).first()
    if db_vehicle:
        raise HTTPException(status_code=400, detail="VIN already exists")
    new_vehicle = models.Vehicle(**vehicle.model_dump())
    new_vehicle.vin = new_vehicle.vin.upper()
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle

@app.put("/vehicle/{vin}", response_model=schemas.VehicleOut)
def update_vehicle(vin: str, vehicle_update: schemas.VehicleBase, db: Session = Depends(get_db)):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.vin == vin).first()
    if not vehicle:
        raise HTTPException(status_code=400, detail="Vehicle not found")
    for key, value in vehicle_update.model_dump(exclude_unset=True).items():
        setattr(vehicle, key, value)
    db.commit()
    db.refresh(vehicle)
    return vehicle
    
@app.delete("/vehicle/{vin}", status_code=204)
def delete_vehicle(vin: str, db: Session = Depends(get_db)):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.vin == vin).first()
    if not vehicle:
        raise HTTPException(status_code=400, detail="Vehicle not found")
    db.delete(vehicle)
    db.commit()
    return