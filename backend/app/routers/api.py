from fastapi import APIRouter, status, HTTPException, Path
from .pydantic_schemas import UserVerification, ResumeRequest
from ..models import User, Resume
from .users import user_dependency_bearer, db_dependency, bcrypt_context


router=APIRouter(
    prefix="/api",
    tags=["api"]
)


@router.get("/users", status_code=status.HTTP_200_OK)
async def read_all_users(user: user_dependency_bearer, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_model = db.query(User).all()
    return user_model



@router.post("/create-resume", status_code=status.HTTP_201_CREATED)
async def create_resume(db: db_dependency,user: user_dependency_bearer,
                        resume_request: ResumeRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    resume_model = Resume(**resume_request.model_dump(), owner_id=user.get("id"))
    db.add(resume_model)
    db.commit()
    db.refresh(resume_model)
    return resume_model


@router.get("/resumes", status_code=status.HTTP_200_OK)
async def read_all_resumes(user: user_dependency_bearer, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    resume_model = db.query(Resume).filter(Resume.owner_id==user.get("id")).all()
    return resume_model


@router.get("/resume/{resume_id}", status_code=status.HTTP_200_OK)
async def read_resume_by_id(db: db_dependency, user: user_dependency_bearer, resume_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    resume_model=db.query(Resume).filter(Resume.id==resume_id, Resume.owner_id==user.get("id")).first()
    if not resume_model:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume_model


@router.put("/update-resume/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_resume(resume_request: ResumeRequest, db: db_dependency, 
                        user: user_dependency_bearer, resume_id :int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    resume_model=db.query(Resume).filter(Resume.id==resume_id, Resume.owner_id==user.get("id")).first()
    if not resume_model:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    resume_model.title=resume_request.title
    resume_model.content=resume_request.content
    
    db.add(resume_model)
    db.commit()
    db.refresh(resume_model)
    return resume_model


@router.delete("/delete-resume/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(db: db_dependency, user: user_dependency_bearer, resume_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    resume_model=db.query(Resume).filter(Resume.id==resume_id, Resume.owner_id==user.get("id")).first()
    if not resume_model:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    db.delete(resume_model)
    db.commit()
    

@router.post("/{resume_id}/improve", status_code=status.HTTP_200_OK)
async def improve_resume(db: db_dependency, user: user_dependency_bearer,
                         resume_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    resume_model=db.query(Resume).filter(Resume.id==resume_id, Resume.owner_id==user.get("id")).first()
    if not resume_model:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    resume_model.content=resume_model.content + " [Improved]"
    db.commit()
    db.refresh(resume_model)
    return resume_model


@router.put("/user/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency_bearer,
                          db: db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail="The user is not authenticated")
    user_model=db.query(User).filter(User.id==user.get('id')).first()
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    user_model.hashed_password=bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()