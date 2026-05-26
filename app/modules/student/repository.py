from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from uuid import UUID
from app.modules.student.models import Student
from app.modules.student.schemas import StudentCreate

class StudentRepository:
    async def get_by_id(self, db: AsyncSession, id: UUID) -> Student | None:
        result = await db.execute(
            select(Student)
            .where(Student.id == id)
            .options(joinedload(Student.user), joinedload(Student.class_))
        )
        return result.scalar_one_or_none()

    async def get_by_student_id(self, db: AsyncSession, student_id: str) -> Student | None:
        result = await db.execute(
            select(Student)
            .where(Student.student_id == student_id)
            .options(joinedload(Student.user), joinedload(Student.class_))
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, db: AsyncSession, user_id: UUID) -> Student | None:
        result = await db.execute(
            select(Student)
            .where(Student.user_id == user_id)
            .options(joinedload(Student.user), joinedload(Student.class_))
        )
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, student_in: StudentCreate) -> Student:
        db_student = Student(
            user_id=student_in.user_id,
            student_id=student_in.student_id,
            class_id=student_in.class_id,
            roll_no=student_in.roll_no,
            gpa=student_in.gpa,
            attendance_rate=student_in.attendance_rate,
            status=student_in.status,
            parent_name=student_in.parent_name,
            parent_email=student_in.parent_email
        )
        db.add(db_student)
        return db_student

student_repo = StudentRepository()
