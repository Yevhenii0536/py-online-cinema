from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.movie import Movie
from schemas import FilmCreate, FilmUpdate
from database import get_db


async def get_movies_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie))
    movies = result.scalars().all()

    return movies


async def create_movie_db(movie: FilmCreate, db: AsyncSession = Depends(get_db)):
    new_movie = Movie(**movie.model_dump())

    db.add(new_movie)

    await db.commit()
    await db.refresh(new_movie)

    return new_movie


async def get_movie_by_id_db(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie).where(Movie.id == movie_id))

    return result.scalar_one_or_none()


async def delete_movie_by_id_db(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalar_one_or_none()

    if not movie:
        return None

    await db.delete(movie)
    await db.commit()

    return movie


async def update_movie_by_id_db(movie_id: int, db: AsyncSession, movie: FilmUpdate):
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    db_movie = result.scalar_one_or_none()

    if not movie:
        return None

    db_movie.title = movie.title
    db_movie.genre = movie.genre
    db_movie.price = movie.price

    await db.commit()
    await db.refresh(db_movie)

    return db_movie
