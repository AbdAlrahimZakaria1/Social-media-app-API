from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.oauth2 import create_access_token
from app.config import settings
from app.main import app
from app.database import get_db
from app import models


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "test_login@example.com", "password": "password123"}
    res = client.post("/api/v1/users", json=user_data)

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "test_login2@example.com", "password": "password12345"}
    res = client.post("/api/v1/users", json=user_data)

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(session, test_user, test_user2):
    posts = [
        {"title": "1st title", "content": "1st content", "owner_id": test_user["id"]},
        {"title": "2st title", "content": "2st content", "owner_id": test_user["id"]},
        {"title": "3st title", "content": "3st content", "owner_id": test_user2["id"]},
    ]

    posts_model_list = [models.Post(**post) for post in posts]
    session.add_all(posts_model_list)
    session.commit()

    posts = session.query(models.Post).all()
    return posts
