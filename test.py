import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from pathlib import Path

#Make SQLite accept Postgres CITEXT
from sqlalchemy.dialects.sqlite.base import SQLiteTypeCompiler

# if not hasattr(SQLiteTypeCompiler, "visit_CITEXT"):
#     SQLiteTypeCompiler.visit_CITEXT = lambda self, type_, **kw: "TEXT"

from app.main import app
from app.database import get_db, Base


# --------------------------------------------------
# Disable lifespan to avoid real DB connections
# --------------------------------------------------
@asynccontextmanager
async def fake_lifespan(app):
    yield


app.router.lifespan_context = fake_lifespan


# --------------------------------------------------
# DB override dependency
# --------------------------------------------------
def override_get_db_session(session_factory):
    def _override():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    return _override


# --------------------------------------------------
# Pytest client fixture (OS-independent)
# --------------------------------------------------
@pytest.fixture(scope="function")
def client(tmp_path: Path):
    db_file = tmp_path / "test_api.sqlite"
    test_db_url = f"sqlite:///{db_file}"

    engine = create_engine(
        test_db_url,
        connect_args={"check_same_thread": False},
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )

    Base.metadata.create_all(bind=engine)

    app.dependency_overrides[get_db] = override_get_db_session(
        TestingSessionLocal
    )

    with TestClient(app) as c:
        yield c

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


# --------------------------------------------------
# Helper
# --------------------------------------------------
def sample_vehicle(vin="1HGBH41JXMN109186"):
    return {
        "vin": vin,
        "manufacturer_name": "Honda",
        "horse_power": 200,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 25000.50,
        "fuel_type": "Gasoline Regular",
        "description": "Reliable sedan"
    }


# --------------------------------------------------
# Tests
# --------------------------------------------------
def test_get_all_empty(client):
    res = client.get("/vehicle")
    assert res.status_code == 200
    assert res.json() == []


def test_create_vehicle(client):
    v = sample_vehicle()
    res = client.post("/vehicle", json=v)
    assert res.status_code == 201
    assert res.json()["vin"] == v["vin"]


def test_get_vehicle_by_vin(client):
    v = sample_vehicle()
    client.post("/vehicle", json=v)

    res = client.get("/vehicle/1HGBH41JXMN109186")
    assert res.status_code == 200
    assert res.json()["manufacturer_name"] == v["manufacturer_name"]


def test_delete_vehicle(client):
    v = sample_vehicle()
    client.post("/vehicle", json=v)

    res = client.delete("/vehicle/1HGBH41JXMN109186")
    assert res.status_code == 204

    res2 = client.get("/vehicle/1HGBH41JXMN109186")
    assert res2.status_code == 400


def test_create_vehicle_invalid_vin_short(client):
    v = sample_vehicle(vin="123")
    res = client.post("/vehicle", json=v)
    assert res.status_code == 422


def test_create_vehicle_invalid_vin_not_alphanumeric(client):
    v = sample_vehicle(vin="1HGBH41JXMN10918!")
    res = client.post("/vehicle", json=v)
    assert res.status_code == 422


def test_create_vehicle_invalid_fuel_type(client):
    v = sample_vehicle()
    v["fuel_type"] = "snapple"
    res = client.post("/vehicle", json=v)
    assert res.status_code == 422


def test_create_duplicate_vehicle(client):
    v = sample_vehicle()
    client.post("/vehicle", json=v)
    res = client.post("/vehicle", json=v)
    assert res.status_code == 400


def test_update_vehicle_success(client):
    v = sample_vehicle()
    client.post("/vehicle", json=v)

    update_data = {
        "manufacturer_name": "Toyota",
        "horse_power": 180,
        "model_name": "Camry",
        "model_year": 2021,
        "purchase_price": 23000.00,
        "fuel_type": "Gasoline Regular",
        "description": "Updated desc"
    }

    res = client.put("/vehicle/1HGBH41JXMN109186", json=update_data)
    assert res.status_code == 200
    assert res.json()["manufacturer_name"] == "Toyota"


def test_update_vehicle_not_found(client):
    update_data = {
        "manufacturer_name": "Test",
        "horse_power": 100,
        "model_name": "Test",
        "model_year": 2020,
        "purchase_price": 10000.00,
        "fuel_type": "Gasoline Regular",
        "description": "Test"
    }

    res = client.put("/vehicle/NOTEXIST123456789", json=update_data)
    assert res.status_code == 400


def test_delete_vehicle_not_found(client):
    res = client.delete("/vehicle/NOTEXIST123456789")
    assert res.status_code == 400


def test_get_all_multiple(client):
    client.post("/vehicle", json=sample_vehicle("11111111111111111"))
    client.post("/vehicle", json=sample_vehicle("22222222222222222"))

    res = client.get("/vehicle")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_create_vehicle_invalid_year(client):
    v = sample_vehicle()
    v["model_year"] = 2029
    res = client.post("/vehicle", json=v)
    assert res.status_code == 422


def test_create_vehicle_invalid_price(client):
    v = sample_vehicle()
    v["purchase_price"] = -5000
    res = client.post("/vehicle", json=v)
    assert res.status_code == 422
