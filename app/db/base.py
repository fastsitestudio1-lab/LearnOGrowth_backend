# app/db/base.py
# Import all the models so that Base.metadata has them loaded before migration or setup
from app.db.base_class import Base
from app.modules.auth.models import User
from app.modules.teacher.models import Teacher
from app.modules.classes.models import Class
from app.modules.student.models import Student
