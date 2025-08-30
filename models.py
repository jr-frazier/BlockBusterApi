from sqlmodel import SQLModel, Field, Column, Integer, String, Boolean, Enum
import enum

class UserRoles(enum.Enum):
    ADMIN = "admin"
    USER = "user"

class Movie(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    title: str = Field(index=True)
    director: str = Field(index=True)
    category: str = Field(index=True)
    rating: int = Field(index=True)
    year_released: int = Field(index=True)
    image_url: str = Field(index=True)
    rental_price: float = Field(index=True)
    available_amount: int = Field(index=True)


class Users(SQLModel, table=True):
    __tablename__ = 'users'
    id: int | None = Field( primary_key=True, index=True)
    email: str = Field( unique=True)
    username: str = Field( unique=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    hashed_password: str
    is_active: bool = Field( default=True)
    role: UserRoles = Field(default=UserRoles.USER)
    phone_number: str = Field(index=True)