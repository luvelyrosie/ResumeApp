import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import Resume, Base, User
from fastapi.testclient import TestClient
from app.main import app
from app.routers.users import bcrypt_context


SQLALCHEMY_DATABASE_URL = "sqlite:///test_resumeapp.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"id": 1, "username": "admin", "email": "abc@abc.com", "role": "admin"}


def override_get_current_user_cookie():
    return {"id": 1, "username": "admin", "email": "abc@abc.com", "role": "admin"}


client=TestClient(app)


@pytest.fixture
def test_resume():
    resume = Resume(
        title="Test Resume",
        content="This is a test resume.",
        owner_id=1  
    )

    db = TestSessionLocal()
    db.add(resume)
    db.commit()
    db.refresh(resume)  
    yield resume

    
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM resumes;"))
        connection.commit()


@pytest.fixture
def test_user():
    db = TestSessionLocal()
    user = User(
        username="admin",
        email="abc@abc.com",
        hashed_password=bcrypt_context.hash("test1234"),
        role="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()