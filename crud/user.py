from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from schemas import UserCreate
from database import get_db
from security import hash_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def create_user_db(db: AsyncSession, user: UserCreate):
    hashed_pwd = hash_password(user.password)

    db_user = User(email=user.email, hashed_password=hashed_pwd)

    db.add(db_user)

    await db.commit()
    await db.refresh(db_user)

    return db_user


async def get_user_by_email_db(email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    return user
