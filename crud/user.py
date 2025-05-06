from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from schemas.user import UserCreate, UserRead
from database import get_db
from security import hash_password, decode_token

security = HTTPBearer()


async def create_user_db(db: AsyncSession, user: UserCreate):
    hashed_pwd = hash_password(user.password)

    db_user = User(email=user.email, hashed_password=hashed_pwd, role="user")

    db.add(db_user)

    await db.commit()
    await db.refresh(db_user)

    return db_user


async def get_user_by_email_db(email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    return user


async def get_current_user_db(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)
) -> UserRead:
    token = credentials.credentials
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    email = payload.get("sub")

    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    db_user = await get_user_by_email_db(db=db, email=email)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserRead.model_validate(db_user)


async def get_users_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))

    return result.scalars().all()


async def require_admin(user: UserRead = Depends(get_current_user_db)):
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    return user


async def make_admin_db(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user_db = result.scalar_one_or_none()

    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_db.role = "admin"

    await db.commit()
    await db.refresh(user_db)

    return { "detail": "Admin privileges granted" }
