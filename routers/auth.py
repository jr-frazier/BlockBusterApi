from datetime import timedelta, timezone, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlmodel import SQLModel
from starlette import status
from passlib.context import CryptContext
from models import Users, UserRoles
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from database import get_session


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


# Key generate with the command: openssl rand -hex 32
SECRET_Key = "112f2dce5dbe5c9aa9d6382f99b6d56e42397227ab5b451f406e72983f1d7d1f"
ALGORITHM = "HS256"

bcrypt_content = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

class CreateUserRequest(SQLModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: str
    role: UserRoles

class Token(SQLModel):
    access_token: str
    token_type: str

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_content.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_Key, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_Key, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

        return {"username": username, "id": user_id, "role": user_role}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: SessionDep, user_request: CreateUserRequest):
    create_user_model = Users(
        email=user_request.email,
        username=user_request.username,
        hashed_password=bcrypt_content.hash(user_request.password),
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        phone_number=user_request.phone_number,
        role=user_request.role
    )

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return create_user_model

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: SessionDep):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(user.username, user.id, user.role.value, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}