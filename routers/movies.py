from typing import Annotated, Optional, List
from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlmodel import Session, select, SQLModel, Field
from sqlalchemy import func
from database import get_session
from models import Movie
from fastapi_pagination import Page, add_pagination, paginate

from routers.auth import get_current_user

SessionDep = Annotated[Session, Depends(get_session)]
user_dependency = Annotated[dict, Depends(get_current_user)]
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
    rental_price: float = Field(ge=0, description="Rental price must be greater than or equal to 0")
    available_amount: int = Field(ge=0, description="Available amount must be greater than or equal to 0")


class UpdateMovie(SQLModel):
    title: Optional[str] = Field(min_length=1, max_length=100, description="Title must be between 1 and 100 characters")
    director: Optional[str] = Field(min_length=1, max_length=100, description="Director must be between 1 and 100 characters")
    category: Optional[str] = Field(min_length=1, max_length=100, description="Category must be between 1 and 100 characters")
    rating: Optional[int] = Field(ge=1, le=5, description="Rating must be between 1 and 5")
    year_released: Optional[int] = Field(ge=1900, lt=2005, description="Year released must be between 1900 and 2005")
    image_url: Optional[str] = Field(min_length=1, max_length=200, description="Image URL must be between 1 and 200 characters")
    rental_price: Optional[float] = Field(ge=0, description="Rental price must be greater than or equal to 0")
    available_amount: Optional[int] = Field(ge=0, description="Available amount must be greater than or equal to 0")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_movies(
    db: SessionDep,
    search: Optional[str] = Query(
        default=None,
        description="Search for movies by title, director, category, or rating"
    ),
    movie_ids: Optional[List[int]] = Query(
        default=None,
        description="Repeat the query param for multiple IDs: ?movie_ids=1&movie_ids=2"
    ),
) -> Page[Movie]:
    if search:
        movies = db.exec(select(Movie).where(func.lower(Movie.title).contains(search.lower()))).all()

        return paginate(movies)

    if movie_ids:
        movies = []
        for movie_id in movie_ids:
            movie = db.get(Movie, movie_id)
            if movie is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="One or more movie IDs not found"
                )
            movies.append(movie)
        return paginate(movies)

    all_movies = db.exec(select(Movie)).all()
    return paginate(all_movies)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_movie(user: user_dependency, movie: AddMovie, db: SessionDep):
    if user is None or user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    db_movie = Movie.model_validate(movie)

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


@router.get("/{movie_id}", status_code=status.HTTP_200_OK)
async def get_movie(movie_id: int, session: SessionDep):
    return session.get(Movie, movie_id)

@router.put("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_movie(user: user_dependency, movie_id: int, movie: UpdateMovie, db: SessionDep):
    if user is None or user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    db_movie = db.get(Movie, movie_id)
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    for key, value in movie.model_dump(exclude_unset=True).items():
        setattr(db_movie, key, value)

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(user: user_dependency, movie_id: int, db: SessionDep):
    if user is None or user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    movie_to_delete = db.get(Movie, movie_id)
    if movie_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    db.delete(movie_to_delete)
    db.commit()

add_pagination(router)
