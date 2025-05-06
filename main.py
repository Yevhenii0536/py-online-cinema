from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

from routers import users, movies, auth
from database import engine
from models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users.router, tags=["Users"])
app.include_router(movies.router, tags=["Movies"])
app.include_router(auth.router, tags=["Auth"])


@app.get("/", include_in_schema=False)
async def redirect_root():
    return RedirectResponse("/docs")
