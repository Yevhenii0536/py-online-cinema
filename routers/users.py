from typing import List

from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, HTTPException, Depends
from schemas.user import UserRead
from crud.user import get_users_db, get_current_user_db, make_admin_db, require_admin

from utils.admin_route import admin_route_depends as depends

router = APIRouter()


@router.get("/users", response_model=List[UserRead], **depends())
async def read_users(db: AsyncSession = Depends(get_db)):
    try:
        return await get_users_db(db=db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/users/me', response_model=UserRead)
def read_me(current_user: UserRead = Depends(get_current_user_db)):
    return current_user


@router.post('/users/{user_id}/make_admin', **depends())
async def make_admin(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await make_admin_db(user_id=user_id, db=db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
