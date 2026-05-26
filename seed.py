import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import SessionLocal, engine
from app.db.base import Base
from app.core.security import get_password_hash
from app.modules.auth.models import User
from app.modules.teacher.models import Teacher
from app.modules.classes.models import Class
from app.modules.student.models import Student

async def seed_data():
    print("Recreating database tables for clean seed...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        print("Inserting seed users...")
        
        # 1. Create Admin User
        admin = User(
            name="Admin User",
            email="admin@nexus.edu",
            password_hash=get_password_hash("admin123"),
            role="admin"
        )
        db.add(admin)

        # 2. Create Teacher User
        teacher_user = User(
            name="Sarah Jenkins",
            email="teacher@nexus.edu",
            password_hash=get_password_hash("teacher123"),
            role="teacher"
        )
        db.add(teacher_user)

        # 3. Create Student Users
        student_user_1 = User(
            name="John Doe",
            email="student1@nexus.edu",
            password_hash=get_password_hash("student123"),
            role="student"
        )
        student_user_2 = User(
            name="Jane Smith",
            email="student2@nexus.edu",
            password_hash=get_password_hash("student123"),
            role="student"
        )
        db.add(student_user_1)
        db.add(student_user_2)

        # Commit Users to get their IDs
        await db.commit()
        await db.refresh(teacher_user)
        await db.refresh(student_user_1)
        await db.refresh(student_user_2)

        # 4. Create Teacher Profile
        teacher_profile = Teacher(
            user_id=teacher_user.id,
            employee_id="EMP-001",
            subject="Mathematics",
            department="Science & Mathematics"
        )
        db.add(teacher_profile)
        await db.commit()
        await db.refresh(teacher_profile)

        # 5. Create Class Master Details
        class_10a = Class(
            grade="10th",
            section="A",
            adviser_id=teacher_profile.id
        )
        class_11b = Class(
            grade="11th",
            section="B",
            adviser_id=None
        )
        db.add(class_10a)
        db.add(class_11b)
        await db.commit()
        await db.refresh(class_10a)
        await db.refresh(class_11b)

        # 6. Create Student Profiles
        student_profile_1 = Student(
            user_id=student_user_1.id,
            student_id="ST-001",
            class_id=class_10a.id,
            roll_no="R-10",
            gpa=3.85,
            attendance_rate=92.50,
            status="Active",
            parent_name="Robert Doe",
            parent_email="parent.doe@example.com"
        )
        student_profile_2 = Student(
            user_id=student_user_2.id,
            student_id="ST-002",
            class_id=class_10a.id,
            roll_no="R-11",
            gpa=2.45,
            attendance_rate=71.20,  # Below 75% -> Warning status is appropriate
            status="Warning",
            parent_name="Mary Smith",
            parent_email="parent.smith@example.com"
        )
        db.add(student_profile_1)
        db.add(student_profile_2)
        await db.commit()

        print("Database seeded successfully with:")
        print("  - Admin: admin@nexus.edu / admin123")
        print("  - Teacher: teacher@nexus.edu / teacher123 (advises 10th-A)")
        print("  - Student 1: student1@nexus.edu / student123 (in 10th-A)")
        print("  - Student 2: student2@nexus.edu / student123 (in 10th-A, status Warning)")

if __name__ == "__main__":
    asyncio.run(seed_data())
