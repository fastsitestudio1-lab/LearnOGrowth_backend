from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, RoleChecker
from app.modules.auth.models import User
from app.modules.teacher.schemas import TeacherCreate, TeacherOut, TeacherDashboardResponse
from app.modules.student.schemas import StudentOut
from app.modules.teacher.service import teacher_service

router = APIRouter()

@router.get("/teacher/dashboard", response_model=TeacherDashboardResponse)
async def get_teacher_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["teacher"]))
):
    return await teacher_service.get_dashboard_data(db, current_user.id)

@router.get("/teacher/students", response_model=list[StudentOut])
async def get_teacher_students(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["teacher"]))
):
    students = await teacher_service.get_roster(db, current_user.id)
    return [StudentOut.model_validate(s) for s in students]

# Admin endpoint to link a user to a teacher profile
@router.post("/teacher", response_model=TeacherOut)
async def create_teacher_profile(
    payload: TeacherCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["admin"]))
):
    teacher = await teacher_service.create_teacher(db, payload)
    return TeacherOut.model_validate(teacher)
