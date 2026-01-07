from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
class UserResponse(BaseModel):
    name: str
    email: EmailStr
