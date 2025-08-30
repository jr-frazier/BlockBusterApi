from typing import Annotated, Optional
from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlmodel import Session, select, SQLModel, Field
from database import get_session
from models import Movie


SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)

class AddMovie(SQLModel):
    title: str = Field(min_length=1, max_length=100, description="Title must be between 1 and 100 characters")
    director: str = Field(min_length=1, max_length=100, description="Director must be between 1 and 100 characters")
    category: str = Field(min_length=1, max_length=100, description="Category must be between 1 and 100 characters")
    rating: int = Field(ge=1, le=5, description="Rating must be between 1 and 5")
    year_released: int = Field(ge=1900, lt=2005, description="Year released must be between 1900 and 2005")
    image_url: str = Field(min_length=1, max_length=200, description="Image URL must be between 1 and 200 characters")


class UpdateMovie(SQLModel):
    title: Optional[str] = Field(min_length=1, max_length=100, description="Title must be between 1 and 100 characters")
    director: Optional[str] = Field(min_length=1, max_length=100, description="Director must be between 1 and 100 characters")
    category: Optional[str] = Field(min_length=1, max_length=100, description="Category must be between 1 and 100 characters")
    rating: Optional[int] = Field(ge=1, le=5, description="Rating must be between 1 and 5")
    year_released: Optional[int] = Field(ge=1900, lt=2005, description="Year released must be between 1900 and 2005")
    image_url: Optional[str] = Field(min_length=1, max_length=200, description="Image URL must be between 1 and 200 characters")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_movies(
    session: SessionDep,
    movie_ids: Optional[list[int]] = Query(default=None, description="Repeat the query param for multiple IDs: ?movie_ids=1&movie_ids=2"),
):
    if movie_ids:
        movies = []
        for movie_id in movie_ids:
            movie = session.get(Movie, movie_id)
            if movie is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more movie IDs not found")
            movies.append(movie)
        return movies

    return session.exec(select(Movie)).all()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_movie(movie: AddMovie, session: SessionDep):
    db_movie = Movie.model_validate(movie)
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie


@router.get("/{movie_id}", status_code=status.HTTP_200_OK)
async def get_movie(movie_id: int, session: SessionDep):
    return session.get(Movie, movie_id)

@router.put("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_movie(movie_id: int, movie: UpdateMovie, session: SessionDep):
    db_movie = session.get(Movie, movie_id)
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    for key, value in movie.model_dump(exclude_unset=True).items():
        setattr(db_movie, key, value)

    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(movie_id: int, session: SessionDep):
    session.delete(session.get(Movie, movie_id))
    session.commit()
    return
