from .utils import *
from app.routers.users import get_db, get_current_user_cookie, get_db
from app.main import app


app.dependency_overrides[get_current_user_cookie] = override_get_current_user_cookie
app.dependency_overrides[get_db] = override_get_db


def test_new_resume_page():
    response = client.get("/resumes/new")
    assert response.status_code == 200
    assert "<form" in response.text 


def test_create_resume():
    data = {"title": "New Resume", "content": "Resume Content"}
    response = client.post("/resumes/new", data=data, follow_redirects=False)
    assert response.status_code == 303 

    db = TestSessionLocal()
    resume = db.query(Resume).filter(Resume.title == "New Resume").first()
    assert resume is not None
    assert resume.content == "Resume Content"


def test_render_list_resumes(test_resume):
    response = client.get("/resumes/")
    assert response.status_code == 200
    assert test_resume.title in response.text


def test_read_resume_by_id(test_resume):
    response = client.get(f"/resumes/{test_resume.id}")
    assert response.status_code == 200
    assert test_resume.title in response.text


def test_read_resume_not_found():
    response = client.get("/resumes/999")
    assert response.status_code == 404
    assert "Resume not found" in response.text


def test_improve_resume(test_resume):
    response = client.post(f"/resumes/{test_resume.id}/improve")
    assert response.status_code == 200
    assert "[Improved]" in response.text

    db = TestSessionLocal()
    resume = db.query(Resume).filter(Resume.id == test_resume.id).first()
    assert "[Improved]" in resume.content