from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import users, resumes, admin, api
from fastapi.templating import Jinja2Templates


app=FastAPI()


Base.metadata.create_all(bind=engine)


templates=Jinja2Templates(directory="frontend/templates")


@app.get("/")
def root():
    return {"message": "Resume App API is running"}


@app.get("/healthy")
def health_check():
    return {"status":"healthy"}


app.include_router(users.router)
app.include_router(resumes.router)
app.include_router(admin.router)
app.include_router(api.router)