from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from uuid import UUID
from app.modules.teacher.models import Teacher
from app.modules.teacher.schemas import TeacherCreate
from app.modules.classes.models import Class
from app.modules.student.models import Student

class TeacherRepository:
    async def get_by_id(self, db: AsyncSession, id: UUID) -> Teacher | None:
        result = await db.execute(
            select(Teacher)
            .where(Teacher.id == id)
            .options(joinedload(Teacher.user))
        )
        return result.scalar_one_or_none()

    async def get_by_employee_id(self, db: AsyncSession, employee_id: str) -> Teacher | None:
        result = await db.execute(
            select(Teacher)
            .where(Teacher.employee_id == employee_id)
            .options(joinedload(Teacher.user))
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, db: AsyncSession, user_id: UUID) -> Teacher | None:
        result = await db.execute(
            select(Teacher)
            .where(Teacher.user_id == user_id)
            .options(joinedload(Teacher.user))
        )
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, teacher_in: TeacherCreate) -> Teacher:
        db_teacher = Teacher(
            user_id=teacher_in.user_id,
            employee_id=teacher_in.employee_id,
            subject=teacher_in.subject,
            department=teacher_in.department
        )
        db.add(db_teacher)
        return db_teacher

    async def get_advised_classes(self, db: AsyncSession, teacher_id: UUID) -> list[Class]:
        result = await db.execute(
            select(Class).where(Class.adviser_id == teacher_id)
        )
        return list(result.scalars().all())

    async def get_students_in_advised_classes(self, db: AsyncSession, teacher_id: UUID) -> list[Student]:
        # 1. Fetch classes advised by teacher
        classes = await self.get_advised_classes(db, teacher_id)
        class_ids = [c.id for c in classes]
        if not class_ids:
            return []
            
        # 2. Fetch students in those classes
        result = await db.execute(
            select(Student)
            .where(Student.class_id.in_(class_ids))
            .options(joinedload(Student.user), joinedload(Student.class_))
        )
        return list(result.scalars().all())

teacher_repo = TeacherRepository()
