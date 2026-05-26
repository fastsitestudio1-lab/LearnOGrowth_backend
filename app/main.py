from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine
from app.core.exceptions import setup_exception_handlers
from app.db.base import Base

# Import module routers
from app.modules.auth.router import router as auth_router
from app.modules.classes.router import router as class_router
from app.modules.student.router import router as student_router
from app.modules.teacher.router import router as teacher_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Automatically create tables for ease of local development and quick testing
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for local development API access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup custom global exception handlers
setup_exception_handlers(app)

# Register routers matching backend API routes specs
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(class_router, prefix="/api", tags=["Classes"])
app.include_router(student_router, prefix="/api", tags=["Students"])
app.include_router(teacher_router, prefix="/api", tags=["Teachers"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Student Nexus API Portal",
        "docs_url": "/docs"
    }
