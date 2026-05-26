from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    name: str = Field(..., max_length=100)
    email: EmailStr
    role: str = Field(..., description="Must be student, teacher, or admin")
    avatar_url: str | None = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserOut(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LoginPayload(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    success: bool
    access_token: str
    user: UserOut

    class Config:
        from_attributes = True

class StandardSuccessResponse(BaseModel):
    success: bool
    message: str
