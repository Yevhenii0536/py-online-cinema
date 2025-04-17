from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from schemas import UserCreate, UserRead, Token
from crud.user import create_user_db, get_user_by_email_db
from security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_db
from models.auth import LoginData

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/user", response_model=UserRead)
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
