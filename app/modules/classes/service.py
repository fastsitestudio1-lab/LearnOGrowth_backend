from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.classes.repository import class_repo
from app.modules.classes.schemas import ClassCreate
from app.modules.classes.models import Class
from app.core.exceptions import ValidationFailedException, ResourceNotFoundException

class ClassService:
    async def get_class(self, db: AsyncSession, class_id: str) -> Class:
        cls = await class_repo.get_by_id(db, class_id)
        if not cls:
            raise ResourceNotFoundException(f"Class with ID {class_id} not found.")
        return cls

    async def create_class(self, db: AsyncSession, class_in: ClassCreate) -> Class:
        existing = await class_repo.get_by_grade_section(db, class_in.grade, class_in.section)
        if existing:
            raise ValidationFailedException(
                message=f"Class {class_in.grade}-{class_in.section} already exists."
            )
        new_class = await class_repo.create(db, class_in)
        await db.commit()
        await db.refresh(new_class)
        return new_class

    async def list_classes(self, db: AsyncSession) -> list[Class]:
        return await class_repo.list_all(db)

class_service = ClassService()
