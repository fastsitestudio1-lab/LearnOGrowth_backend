from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from app.modules.auth.schemas import UserOut
from app.modules.classes.schemas import ClassOut

class StudentBase(BaseModel):
    student_id: str = Field(..., description="Student ID (e.g. ST-001)")
    class_id: UUID
    roll_no: str
    gpa: float = Field(default=0.0, ge=0.0, le=4.0)
    attendance_rate: float = Field(default=100.0, ge=0.0, le=100.0)
    status: str = Field(default="Active", description="Active, Warning, Inactive")
    parent_name: str
    parent_email: EmailStr | None = None

class StudentCreate(StudentBase):
    user_id: UUID

class StudentOut(StudentBase):
    id: UUID
    created_at: datetime
    user: UserOut
    class_: ClassOut = Field(..., alias="class_")

    class Config:
        from_attributes = True
        populate_by_name = True

class StudentDashboardResponse(BaseModel):
    student_id: str
    roll_no: str
    gpa: float
    attendance_rate: float
    status: str
    class_name: str
    upcoming_assignments: list[dict] = []
    recent_grades: list[dict] = []
    recent_notifications: list[dict] = []
