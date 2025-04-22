from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.movie import MovieCreate, MovieRead, MovieUpdate
from database import get_db

from crud.movie import get_movies_db, create_movie_db, get_movie_by_id_db, delete_movie_by_id_db, update_movie_by_id_db


router = APIRouter()

@router.get("/movies", response_model=List[MovieRead])
async def read_movies(db: AsyncSession = Depends(get_db)):
    try:
        movies = await get_movies_db(db=db)
        return movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/movies", response_model=MovieRead)
async def create_movie(movie: MovieCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_movie_db(movie=movie, db=db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/movies/{movie_id}", response_model=MovieRead)
async def read_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await get_movie_by_id_db(movie_id=movie_id, db=db)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.put("/movies/{movie_id}", response_model=MovieRead)
async def update_movie(movie_id: int, movie: MovieUpdate, db: AsyncSession = Depends(get_db)):
    updated_movie = await update_movie_by_id_db(movie_id=movie_id, db=db, movie=movie)

    if not updated_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated_movie


@router.delete("/movies/{movie_id}", response_model=MovieRead)
async def remove_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await delete_movie_by_id_db(movie_id=movie_id, db=db)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie
