from sqlmodel import SQLModel, Field


class Movie(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    title: str = Field(index=True)
    director: str = Field(index=True)
    category: str = Field(index=True)
    rating: int = Field(index=True)
    year_released: int = Field(index=True)
    image_url: str = Field(index=True)