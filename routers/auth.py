from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from schemas.user import UserCreate, UserRead
from schemas.token import Token
from crud.user import create_user_db, get_user_by_email_db
from security import verify_password, hash_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_db
from models.auth import LoginData

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email_db(email=user.email, db=db)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user_db(db=db, user=user)


@router.post("/login", response_model=Token)
async def login(data: LoginData, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email_db(email=data.email, db=db)

    if db_user is None or not verify_password(data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/reset-password")
async def reset_password(email: str, new_password: str, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email_db(db=db, email=email)

    is_same_pwd = verify_password(new_password, db_user.hashed_password)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if is_same_pwd:
        raise HTTPException(status_code=400, detail="New password is the same as old password")

    db_user.hashed_password = hash_password(new_password)

    await db.commit()

    return {"detail": "Password updated"}