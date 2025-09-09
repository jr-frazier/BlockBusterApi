from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from database import create_db_and_tables
from routers import movies, users, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
        "http://localhost:8000",  # Example for FastAPI's default port
        "http://localhost:3000",  # Example for a common frontend framework port
        # Add other specific origins if needed, e.g., "https://your-frontend-domain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movies.router)
app.include_router(users.router)

app.include_router(auth.router)


