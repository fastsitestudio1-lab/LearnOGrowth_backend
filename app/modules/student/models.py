from __future__ import annotations
import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.modules.auth.models import User
    from app.modules.classes.models import Class

class Student(Base):
    __tablename__ = "students"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    student_id: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    class_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("classes.id"), nullable=False)
    roll_no: Mapped[str] = mapped_column(String(20), nullable=False)
    gpa: Mapped[float] = mapped_column(Numeric(3, 2), default=0.00)
    attendance_rate: Mapped[float] = mapped_column(Numeric(5, 2), default=100.00)
    status: Mapped[str] = mapped_column(String(20), default="Active")  # Active, Warning, Inactive
    parent_name: Mapped[str] = mapped_column(String(100), nullable=False)
    parent_email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user: Mapped[User] = relationship(back_populates="student")
    class_: Mapped[Class] = relationship(foreign_keys=[class_id], back_populates="students")
