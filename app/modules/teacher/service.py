from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.teacher.repository import teacher_repo
from app.modules.teacher.schemas import TeacherCreate
from app.modules.teacher.models import Teacher
from app.modules.student.models import Student
from app.core.exceptions import ResourceNotFoundException, ValidationFailedException

class TeacherService:
    async def get_profile_by_user(self, db: AsyncSession, user_id: str) -> Teacher:
        teacher = await teacher_repo.get_by_user_id(db, user_id)
        if not teacher:
            raise ResourceNotFoundException("Teacher profile not found for the given user.")
        return teacher

    async def create_teacher(self, db: AsyncSession, teacher_in: TeacherCreate) -> Teacher:
        existing = await teacher_repo.get_by_employee_id(db, teacher_in.employee_id)
        if existing:
            raise ValidationFailedException(
                message=f"Employee ID {teacher_in.employee_id} is already registered."
            )

        async with db.begin():
            new_teacher = await teacher_repo.create(db, teacher_in)
            
        await db.refresh(new_teacher)
        return await teacher_repo.get_by_id(db, new_teacher.id)

    async def get_dashboard_data(self, db: AsyncSession, user_id: str) -> dict:
        teacher = await self.get_profile_by_user(db, user_id)
        
        # Count classes advised by teacher
        classes = await teacher_repo.get_advised_classes(db, teacher.id)
        class_count = len(classes)
        
        # Count students in advised classes
        students = await teacher_repo.get_students_in_advised_classes(db, teacher.id)
        active_student_count = len(students)
        
        return {
            "class_count": class_count,
            "active_student_count": active_student_count,
            "pending_assignments": 0,
            "pending_leave_approvals": 0
        }

    async def get_roster(self, db: AsyncSession, user_id: str) -> list[Student]:
        teacher = await self.get_profile_by_user(db, user_id)
        return await teacher_repo.get_students_in_advised_classes(db, teacher.id)

teacher_service = TeacherService()
