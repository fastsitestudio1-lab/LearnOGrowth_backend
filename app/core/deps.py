from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import AsyncGenerator

from app.core.database import SessionLocal
from app.core.security import decode_access_token
from app.core.exceptions import CredentialsMismatchException, ForbiddenException

# Note: We import User from its location. Since deps doesn't import router, this prevents circular dependencies.
from app.modules.auth.models import User

security_bearer = HTTPBearer(auto_error=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
    token_bearer: HTTPAuthorizationCredentials = Depends(security_bearer)
) -> User:
    # Try cookie first
    token = request.cookies.get("nexus-token")
    
    # Fallback to Authorization Header
    if not token and token_bearer:
        token = token_bearer.credentials
        
    if not token:
        raise CredentialsMismatchException("Not authenticated.")
        
    payload = decode_access_token(token)
    import uuid
    user_id = payload.get("sub")
    if not user_id:
        raise CredentialsMismatchException("Invalid token payload.")
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise CredentialsMismatchException("Invalid token format.")
        
    result = await db.execute(select(User).where(User.id == user_uuid))
    user = result.scalar_one_or_none()
    if not user:
        raise CredentialsMismatchException("User not found.")
    return user

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise ForbiddenException(
                message=f"Role '{current_user.role}' is not authorized to access this resource."
            )
        return current_user
