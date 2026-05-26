from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.core.deps import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.modules.auth.schemas import LoginPayload, LoginResponse, UserCreate, UserOut, StandardSuccessResponse
from app.modules.auth.service import auth_service

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def login(
    payload: LoginPayload,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    user = await auth_service.authenticate(db, payload.email, payload.password)
    
    # Create Access Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=access_token_expires
    )
    
    # Set Cookies
    # 1. nexus-token: HttpOnly JWT Cookie
    response.set_cookie(
        key="nexus-token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/"
    )
    
    # 2. nexus-role: Accessible role cookie for client-side routing check
    response.set_cookie(
        key="nexus-role",
        value=user.role,
        httponly=False,
        secure=False,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/"
    )
    
    return LoginResponse(
        success=True,
        access_token=access_token,
        user=UserOut.model_validate(user)
    )

@router.post("/logout", response_model=StandardSuccessResponse)
async def logout(response: Response):
    # Clear cookies
    response.delete_cookie(key="nexus-token", path="/")
    response.delete_cookie(key="nexus-role", path="/")
    return StandardSuccessResponse(success=True, message="Successfully logged out.")

@router.post("/register", response_model=UserOut)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    user = await auth_service.create_user(db, user_in)
    return UserOut.model_validate(user)
