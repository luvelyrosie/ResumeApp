from .utils import *
from fastapi import status
from app.routers.users import get_db, get_current_user_bearer, get_db
from app.main import app


app.dependency_overrides[get_current_user_bearer] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db


def test_admin_read_all_resumes_authenticated(test_resume):
    response = client.get("/admin/resumes")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data[0]["id"] == test_resume.id
    assert data[0]["title"] == test_resume.title


def test_admin_delete_resume(test_resume):
    response = client.delete(f"/admin/resumes/{test_resume.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestSessionLocal()
    model = db.query(Resume).filter(Resume.id == test_resume.id).first()
    assert model is None


def test_admin_delete_resume_not_found():
    response = client.delete("/admin/resumes/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Resume not found"}


def test_admin_read_all_users_authenticated(test_user):
    response = client.get("/admin/users")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert any(u["id"] == test_user.id for u in data)


def test_admin_delete_user(test_user):
    response = client.delete(f"/admin/users/{test_user.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestSessionLocal()
    model = db.query(User).filter(User.id == test_user.id).first()
    assert model is None


def test_admin_delete_user_not_found():
    response = client.delete("/admin/users/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}