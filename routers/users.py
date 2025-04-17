# from typing import List

from fastapi import APIRouter

# from fastapi.params import Depends
#
# from dependencies.auth import get_current_user
# from models.user import User

router = APIRouter()


# async def read_users(users: List[User] = Depends(get_current_user)):
@router.get("/users")
async def read_users():
    return {"message": "Hello, World, users!"}
