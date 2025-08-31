from fastapi import APIRouter, HTTPException, Path
from starlette import status
from ..models import User, Resume
from .users import user_dependency_bearer, db_dependency


router=APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@router.get("/users", status_code=status.HTTP_200_OK)
async def read_all_users(user: user_dependency_bearer, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail="Failed authentication")
    return db.query(User).all()


@router.get("/resumes", status_code=status.HTTP_200_OK)
async def read_all_resumes(user: user_dependency_bearer, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail="Failed authentication")
    return db.query(Resume).all()


@router.delete("/resumes/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(user: user_dependency_bearer, 
                      db: db_dependency, 
                      resume_id: int=Path(gt=0)):
    if user is None or user.get('role') !='admin':
        raise HTTPException(status_code=401, detail="Failed authentication")
    resume_model=db.query(Resume).filter(Resume.id==resume_id).first()
    if resume_model is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    db.query(Resume).filter(Resume.id==resume_id).delete()
    db.commit()
    
    
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: user_dependency_bearer, 
                      db: db_dependency, 
                      user_id: int=Path(gt=0)):
    if user is None or user.get('role') !='admin':
        raise HTTPException(status_code=401, detail="Failed authentication")
    user_model=db.query(User).filter(User.id==user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.query(User).filter(User.id==user_id).delete()
    db.commit()