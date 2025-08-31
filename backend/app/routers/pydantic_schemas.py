from pydantic import BaseModel, Field, EmailStr


class UserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str
   
    
class ResumeRequest(BaseModel):
    title: str = Field(min_length=3)
    content: str = Field(min_length=10)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class UserVerification(BaseModel):
    password: str
    new_password: str=Field(min_length=6)