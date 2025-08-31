from fastapi import status
from .utils import *
from app.routers.users import get_db, get_current_user_bearer, get_db
from app.main import app


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user_bearer] = override_get_current_user


def test_read_all_users_authenticated(test_user):
    token = client.post(
        "/user/token",
        data={"username": "admin", "password": "test1234"}
    ).json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/users", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    
    users = response.json()
    assert users[0]["username"] == test_user.username
    assert users[0]["email"] == test_user.email
    assert users[0]["role"] == test_user.role




def test_read_all_resumes_authenticated(test_resume):
    response = client.get("/api/resumes")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data[0]["id"] == test_resume.id
    assert data[0]["title"] == test_resume.title
    assert data[0]["content"] == test_resume.content
    assert data[0]["owner_id"] == test_resume.owner_id


def test_read_resume_by_id_authenticated(test_resume):
    response = client.get(f"/api/resume/{test_resume.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_resume.id
    assert data["title"] == test_resume.title
    assert data["content"] == test_resume.content


def test_read_resume_not_found():
    response = client.get("/api/resume/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Resume not found"}


def test_create_resume():
    request_data = {"title": "New Resume", "content": "Resume Content"}
    response = client.post("/api/create-resume", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestSessionLocal()
    model = db.query(Resume).filter(Resume.title == "New Resume").first()
    assert model is not None
    assert model.title == request_data["title"]
    assert model.content == request_data["content"]


def test_update_resume(test_resume):
    request_data = {"title": "Updated Resume", "content": "Updated Content"}
    response = client.put(f"/api/update-resume/{test_resume.id}", json=request_data)
    assert response.status_code == status.HTTP_200_OK or response.status_code == 204

    db = TestSessionLocal()
    model = db.query(Resume).filter(Resume.id == test_resume.id).first()
    assert model.title == request_data["title"]
    assert model.content == request_data["content"]


def test_update_resume_not_found():
    request_data = {"title": "Updated Resume", "content": "Updated Content"}
    response = client.put("/api/update-resume/999", json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Resume not found"}


def test_delete_resume(test_resume):
    response = client.delete(f"/api/delete-resume/{test_resume.id}")
    assert response.status_code == 204

    db = TestSessionLocal()
    model = db.query(Resume).filter(Resume.id == test_resume.id).first()
    assert model is None


def test_delete_resume_not_found():
    response = client.delete("/api/delete-resume/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Resume not found"}


def test_improve_resume(test_resume):
    response = client.post(f"/api/{test_resume.id}/improve")
    assert response.status_code == status.HTTP_200_OK
    db = TestSessionLocal()
    model = db.query(Resume).filter(Resume.id == test_resume.id).first()
    assert "[Improved]" in model.content
