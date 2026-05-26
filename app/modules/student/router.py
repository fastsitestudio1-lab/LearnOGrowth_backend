from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, RoleChecker, get_current_user
from app.modules.auth.models import User
from app.modules.student.schemas import StudentCreate, StudentOut, StudentDashboardResponse
from app.modules.student.service import student_service

router = APIRouter()

@router.get("/student/dashboard", response_model=StudentDashboardResponse)
async def get_student_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["student"]))
):
    return await student_service.get_dashboard_data(db, current_user.id)

@router.get("/student/profile", response_model=StudentOut)
async def get_student_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["student"]))
):
    student = await student_service.get_profile_by_user(db, current_user.id)
    return StudentOut.model_validate(student)

# Admin endpoint to link a user to a student profile
@router.post("/student", response_model=StudentOut)
async def create_student_profile(
    payload: StudentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["admin"]))
):
    student = await student_service.create_student(db, payload)
    return StudentOut.model_validate(student)
