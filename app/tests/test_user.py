from app import schemas
from .database import client, session


def test_root(client):
    response = client.get("/")
    assert response.json().get("message") == "Hello World"


def test_create_user(client):
    response = client.post(
        "/api/v1/users",
        json={"email": "example123@example.com", "password": "password123"},
    )
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "example123@example.com"
    assert response.status_code == 201
