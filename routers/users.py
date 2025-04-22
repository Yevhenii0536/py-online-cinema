from typing import List
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, HTTPException, Depends
from schemas.user import UserRead
from crud.user import get_users_db, get_current_user_db

router = APIRouter()


@router.get("/users", response_model=List[UserRead])
async def read_users(db: AsyncSession = Depends(get_db)):
    try:
        return await get_users_db(db=db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/me')
def read_me(current_user: UserRead = Depends(get_current_user_db)):
    return current_user