import pytest
from app import schemas
from app.config import settings
from jose import jwt

test_incorrect_login_input = [
    ("test_login@example.com", "wrongPassword", 403),
    ("wrong_login@example.com", "password123", 403),
    ("wrong_login@example.com", "wrongPassword", 403),
    (None, "wrongPassword", 422),
    ("test_login@example.com", None, 422),
]


def test_create_user(client):
    res = client.post(
        "/api/v1/users",
        json={"email": "example123@example.com", "password": "password123"},
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "example123@example.com"
    assert res.status_code == 201


def test_login(client, test_login_data):
    res = client.post(
        "/api/v1/login",
        data={
            "username": test_login_data["email"],
            "password": test_login_data["password"],
        },
    )

    token_data = schemas.Token(**res.json())
    payload = jwt.decode(
        token_data.access_token,
        settings.jwt_secret_key,
        algorithms=[settings.algorithm],
    )
    user_id = payload.get("user_id")
    assert user_id == test_login_data["id"]
    assert res.status_code == 200
    assert token_data.token_type == "bearer"


@pytest.mark.parametrize("email, password, status_code", test_incorrect_login_input)
def test_incorrect_login(client, email, password, status_code):
    res = client.post(
        "/api/v1/login",
        data={
            "username": email,
            "password": password,
        },
    )
    assert res.status_code == status_code
