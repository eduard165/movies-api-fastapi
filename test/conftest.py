import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.conexion import connect_to_db, close_db_connection

# Fixture para el cliente de pruebas
@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module")
async def local_db():
    await connect_to_db()
    yield  
    await close_db_connection()
