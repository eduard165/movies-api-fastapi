import pytest
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_login_success(test_client):
    response = test_client.post("/auth/login", data={
        "email": "user@example.com",
        "password": "string"
    })
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_login_failure(test_client):
    response = test_client.post("/auth/login", data={
        "email": "wronguser@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401  

@pytest.mark.asyncio
async def test_read_users_me(test_client):
    response = test_client.post("/auth/login", data={
        "email": "user@example.com",
        "password": "string"
    })
    token = response.json().get("access_token")
    response = test_client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_read_users_me_no_token(test_client):
    response = test_client.get("/auth/me")
    assert response.status_code == 401  
