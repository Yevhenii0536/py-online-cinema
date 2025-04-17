from fastapi.security import OAuth2PasswordBearer
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import UserRead
from security import decode_token
from fastapi import Depends, HTTPException
from crud import get_user_by_email_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
) -> UserRead:
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload.get("sub")

    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    db_user = await get_user_by_email_db(email, db=db)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserRead.model_validate(db_user)
