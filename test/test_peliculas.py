import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.mark.asyncio
async def test_login_success(test_client):
    response = test_client.post("/auth/login", data={
        "email": "user@example.com",
        "password": "string"
    })
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_peliculas(test_client):
    token = await test_login_success()  
    response = test_client.get("/peliculas/obtener_todas_las_peliculas", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_pelicula(test_client):
    token = await test_login_success()  
    response = test_client.post("/peliculas/registrar_pelicula", json={
        "nombre": "Pelicula de prueba",
        "actores": ["Actor1", "Actor2"],
        "director": "Director de prueba",
        "genero": "Acción",
        "calificacion": 8,
        "anio_lanzamiento": 2024
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    pelicula = response.json()
    assert pelicula["nombre"] == "Pelicula de prueba"
    assert pelicula["genero"] == "Acción"
    assert pelicula["anio_lanzamiento"] == 2024


@pytest.mark.asyncio
async def test_get_pelicula_by_id(test_client):
    token = await test_login_success() 
    response = test_client.get("/peliculas/obtener_pelicula_por_id/673a95028f4f13f96a0a6c7e", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    pelicula = response.json()
    assert "nombre" in pelicula
    assert "actores" in pelicula


@pytest.mark.asyncio
async def test_update_pelicula(test_client):
    token = await test_login_success()  
    response = test_client.put("/peliculas/actualizar_pelicula/673a95028f4f13f96a0a6c7e", json={
        "nombre": "Pelicula Actualizada",
        "actores": ["Actor1", "Actor3"],
        "director": "Director Actualizado",
        "genero": ["Comedia"],
        "calificacion": 9,
        "anio_lanzamiento": 2025
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    pelicula = response.json()
    assert pelicula["nombre"] == "Pelicula Actualizada"
    assert pelicula["genero"] == "Comedia"
    assert pelicula["anio_lanzamiento"] == 2025


@pytest.mark.asyncio
async def test_delete_pelicula(test_client):
    token = await test_login_success()  
    response = test_client.delete("/peliculas/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"detail": "Pelicula eliminada con éxito"}
