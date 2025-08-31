from .database import Base
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__="users"
    
    id=Column(Integer, primary_key=True, index=True)
    username=Column(String, unique=True, index=True, nullable=False)
    email=Column(String, unique=True, index=True, nullable=False)
    hashed_password=Column(String)
    role=Column(String)
    
    resumes=relationship("Resume", back_populates="owner")
    
    
class Resume(Base):
    __tablename__="resumes"
    
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String)
    content=Column(Text)
    owner_id=Column(Integer, ForeignKey("users.id"))
    
    owner=relationship("User", back_populates="resumes")