from typing import Annotated, Optional
from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlmodel import Session, select, SQLModel, Field
from database import get_session
from models import Users

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

class AddUser(SQLModel):
    email: str = Field(min_length=1, max_length=100, description="Email must be between 1 and 100 characters")
    username: str = Field(min_length=1, max_length=100, description="Username must be between 1 and 100 characters")
    first_name: str = Field(min_length=1, max_length=100, description="First name must be between 1 and 100 characters")
    last_name: str = Field(min_length=1, max_length=100, description="Last name must be between 1 and 100 characters")
    password: str = Field(min_length=8, max_length=100, description="Password must be between 8 and 100 characters")

@router.get("/", response_model=list[Users], status_code=status.HTTP_200_OK)
async def get_all_users(session: SessionDep):
    return session.exec(select(Users)).all()

@router.get("/{user_id}", response_model=Users, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, session: SessionDep):
    user = session.exec(select(Users).where(Users.id == user_id)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
