from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models
from . import schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vehicle APIs")

@app.get("/vehicles/", response_model=list[schemas.VehicleOut])
def get_vehicles(db: Session = Depends(get_db)):
    return db.query(models.Vehicle).all()