from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.deps import get_db, RoleChecker
from app.modules.classes.schemas import ClassCreate, ClassOut
from app.modules.classes.service import class_service

router = APIRouter()

# Admin-only route to create classes
@router.post("/admin/classes", response_model=ClassOut)
async def create_class(
    payload: ClassCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(RoleChecker(["admin"]))
):
    cls = await class_service.create_class(db, payload)
    return ClassOut.model_validate(cls)

# General authenticated route to list classes
@router.get("/classes", response_model=list[ClassOut])
async def list_classes(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(RoleChecker(["admin", "teacher", "student"]))
):
    classes = await class_service.list_classes(db)
    return [ClassOut.model_validate(c) for c in classes]
