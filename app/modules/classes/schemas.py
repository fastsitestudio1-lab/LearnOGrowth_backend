from pydantic import BaseModel, Field
from uuid import UUID

class ClassBase(BaseModel):
    grade: str = Field(..., description="Grade (e.g. '10th', '11th')")
    section: str = Field(..., description="Section (e.g. 'A', 'B')")
    adviser_id: UUID | None = None

class ClassCreate(ClassBase):
    pass

class ClassOut(ClassBase):
    id: UUID

    class Config:
        from_attributes = True
