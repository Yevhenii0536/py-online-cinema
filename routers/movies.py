from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import FilmCreate, FilmRead, FilmUpdate
from database import get_db

from crud import get_movies, create_movie, get_movie_by_id, delete_movie_by_id, update_movie_by_id


router = APIRouter()
# // s
@router.get("/movies", response_model=List[FilmRead])
async def read_movies(db: AsyncSession = Depends(get_db)):
    try:
        movies = await get_movies(db)
        return movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/movies", response_model=FilmRead)
async def create_movie(movie: FilmCreate, db: AsyncSession = Depends(get_db)):
    try:
        return create_movie(movie, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/movies/{movie_id}", response_model=FilmRead)
async def read_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await get_movie_by_id(movie_id, db)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.put("/movies/{movie_id}", response_model=FilmRead)
async def update_movie(movie_id: int, movie: FilmUpdate, db: AsyncSession = Depends(get_db)):
    updated_movie = await update_movie_by_id(movie_id=movie_id, db=db, movie=movie)

    if not updated_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated_movie


@router.delete("/movies/{movie_id}", response_model=FilmRead)
async def remove_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await delete_movie_by_id(movie_id, db)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie
