from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.modules.classes.models import Class
from app.modules.classes.schemas import ClassCreate

class ClassRepository:
    async def get_by_id(self, db: AsyncSession, class_id: UUID) -> Class | None:
        result = await db.execute(select(Class).where(Class.id == class_id))
        return result.scalar_one_or_none()

    async def get_by_grade_section(self, db: AsyncSession, grade: str, section: str) -> Class | None:
        result = await db.execute(
            select(Class).where(Class.grade == grade, Class.section == section)
        )
        return result.scalar_one_or_none()

    async def list_all(self, db: AsyncSession) -> list[Class]:
        result = await db.execute(select(Class))
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, class_in: ClassCreate) -> Class:
        db_class = Class(
            grade=class_in.grade,
            section=class_in.section,
            adviser_id=class_in.adviser_id
        )
        db.add(db_class)
        return db_class

class_repo = ClassRepository()
