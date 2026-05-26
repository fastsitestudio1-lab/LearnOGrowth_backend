from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.auth.repository import user_repo
from app.modules.auth.schemas import UserCreate
from app.modules.auth.models import User
from app.core.security import verify_password
from app.core.exceptions import CredentialsMismatchException, ValidationFailedException

class AuthService:
    async def authenticate(self, db: AsyncSession, email: str, password: str) -> User:
        user = await user_repo.get_by_email(db, email)
        if not user:
            raise CredentialsMismatchException("Invalid email or password.")
        if not verify_password(password, user.password_hash):
            raise CredentialsMismatchException("Invalid email or password.")
        return user

    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        # Check if email already exists
        existing_user = await user_repo.get_by_email(db, user_in.email)
        if existing_user:
            raise ValidationFailedException(
                message="A user with this email address already exists.",
                details={"email": "Email already registered"}
            )
        
        new_user = await user_repo.create(db, user_in)
        await db.commit()
        # Refresh inside active session to populate IDs
        await db.refresh(new_user)
        return new_user

auth_service = AuthService()
