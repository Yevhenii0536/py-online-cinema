from fastapi import FastAPI
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

app.include_router(users.router)
app.include_router(movies.router)
app.include_router(auth.router)


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
