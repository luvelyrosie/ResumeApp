from fastapi import APIRouter, Form, HTTPException, Request, status, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from ..models import Resume
from .users import user_dependency_cookie, db_dependency
from fastapi.responses import RedirectResponse


router = APIRouter(
    prefix="/resumes",
    tags=["resume"]
)


templates = Jinja2Templates(directory="frontend/templates")


@router.get("/new")
async def new_resume_page(request: Request, user: user_dependency_cookie):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return templates.TemplateResponse(request, "new_resume.html", {"request": request})


@router.post("/new")
async def create_resume(db: db_dependency,user: user_dependency_cookie,
                        request: Request,title: str = Form(...),content: str = Form(...)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    resume_model = Resume(title=title, content=content, owner_id=user.get("id"))
    db.add(resume_model)
    db.commit()
    db.refresh(resume_model)
    
    return RedirectResponse(url="/resumes/", status_code=303)



@router.get("/")
async def render_list_resumes(request: Request, user: user_dependency_cookie, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    resume_model = db.query(Resume).filter(Resume.owner_id==user.get("id"))
    return templates.TemplateResponse(request, "resumes.html", {"request": request, "resumes": resume_model})



@router.get("/{resume_id}", response_class=HTMLResponse)
async def read_resume_by_id(request: Request, resume_id: int, user: user_dependency_cookie, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    resume_model = db.query(Resume).filter(Resume.id==resume_id, Resume.owner_id==user.get("id")).first()
    if not resume_model:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    return templates.TemplateResponse(request, "resume_detail.html", {"request": request, "resume": resume_model})


@router.post("/{resume_id}/improve", response_class=HTMLResponse)
async def improve_resume(db: db_dependency, user: user_dependency_cookie,
                         request: Request,resume_id: int = Path(gt=0),):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    resume_model = db.query(Resume).filter(Resume.id == resume_id,Resume.owner_id == user.get("id")).first()
    
    if not resume_model:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    resume_model.content += " [Improved]"
    db.commit()
    db.refresh(resume_model)
    
    return templates.TemplateResponse(
        request,
        "resume_detail.html",
        {
            "request": request,
            "resume": resume_model,
            "improved": resume_model.content
        }
    )