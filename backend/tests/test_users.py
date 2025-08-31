from .utils import *
from fastapi import status
from app.routers.users import get_db, get_current_user_bearer, get_db


app.dependency_overrides[get_current_user_bearer] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db


def test_register_user():
    request_data = {
        "username": "newuser",
        "email": "newuser@test.com",
        "password": "password123",
        "role": "user"
    }
    response = client.post("/user/register", data=request_data, follow_redirects=False)
    assert response.status_code == status.HTTP_303_SEE_OTHER


def test_login_user(test_user):
    response = client.post(
        "/user/login",
        data={"username": "admin", "password": "test1234"},
        follow_redirects=False
    )
    assert response.status_code == status.HTTP_303_SEE_OTHER


def test_login_user_invalid():
    response = client.post(
        "/user/login",
        data={"username": "wronguser", "password": "wrongpass"}
    )
    assert response.status_code == 200
    assert "Invalid email or password" in response.text


def test_token_endpoint(test_user: User):
    response = client.post(
        "/user/token",
        data={"username": "admin", "password": "test1234"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    json_data = response.json()
    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"
