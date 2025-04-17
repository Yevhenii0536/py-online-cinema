from fastapi import APIRouter
from uuid import UUID


router = APIRouter()

@router.get("/users")
async def read_users():
    return {"message": "Hello, World, users!"}