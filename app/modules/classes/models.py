from __future__ import annotations
import uuid
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.modules.teacher.models import Teacher
    from app.modules.student.models import Student

class Class(Base):
    __tablename__ = "classes"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    grade: Mapped[str] = mapped_column(String(20), nullable=False)
    section: Mapped[str] = mapped_column(String(10), nullable=False)
    adviser_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True)

    # Constraints
    __table_args__ = (
        UniqueConstraint("grade", "section", name="uq_grade_section"),
    )

    # Relationships
    adviser: Mapped[Teacher | None] = relationship(back_populates="advised_classes")
    students: Mapped[list[Student]] = relationship(back_populates="class_")
