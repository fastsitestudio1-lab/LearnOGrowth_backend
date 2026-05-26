from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from app.modules.auth.schemas import UserOut

class TeacherBase(BaseModel):
    employee_id: str = Field(..., description="Employee ID (e.g. EMP-001)")
    subject: str = Field(..., description="Primary subject taught")
    department: str = Field(..., description="Department name")

class TeacherCreate(TeacherBase):
    user_id: UUID

class TeacherOut(TeacherBase):
    id: UUID
    created_at: datetime
    user: UserOut

    class Config:
        from_attributes = True

class TeacherDashboardResponse(BaseModel):
    class_count: int
    active_student_count: int
    pending_assignments: int = 0
    pending_leave_approvals: int = 0
