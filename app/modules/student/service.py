from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.student.repository import student_repo
from app.modules.student.schemas import StudentCreate
from app.modules.student.models import Student
from app.modules.classes.repository import class_repo
from app.core.exceptions import ResourceNotFoundException, ValidationFailedException

class StudentService:
    async def get_profile_by_user(self, db: AsyncSession, user_id: str) -> Student:
        student = await student_repo.get_by_user_id(db, user_id)
        if not student:
            raise ResourceNotFoundException("Student profile not found for the given user.")
        return student

    async def create_student(self, db: AsyncSession, student_in: StudentCreate) -> Student:
        # Check if student ID already exists
        existing = await student_repo.get_by_student_id(db, student_in.student_id)
        if existing:
            raise ValidationFailedException(
                message=f"Student ID {student_in.student_id} is already registered."
            )
        
        # Check if class exists
        cls = await class_repo.get_by_id(db, student_in.class_id)
        if not cls:
            raise ResourceNotFoundException(f"Class with ID {student_in.class_id} not found.")

        new_student = await student_repo.create(db, student_in)
        await db.commit()
        await db.refresh(new_student)
        # Fetch fully populated model (with relationship loads)
        return await student_repo.get_by_id(db, new_student.id)

    async def get_dashboard_data(self, db: AsyncSession, user_id: str) -> dict:
        student = await self.get_profile_by_user(db, user_id)
        
        class_name = f"{student.class_.grade}-{student.class_.section}"
        
        # Return mock elements for assignments, grades, and notifications for Phase 1 compatibility
        return {
            "student_id": student.student_id,
            "roll_no": student.roll_no,
            "gpa": float(student.gpa),
            "attendance_rate": float(student.attendance_rate),
            "status": student.status,
            "class_name": class_name,
            "upcoming_assignments": [],
            "recent_grades": [],
            "recent_notifications": []
        }

student_service = StudentService()
