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
        print(f"Returning {len(vehicles)} vehicles")
        return vehicles
    except Exception as e:
        print("Error in get_vehicles:", e)  # prints to terminal
        raise HTTPException(status_code=500, detail=str(e))
    
#uvicorn app.main:app --reload
# curl http://127.0.0.1:8000/vehicle