from contextlib import asynccontextmanager
import models
from database import engine
from fastapi import FastAPI

from database import create_db_and_tables
from routers import movies

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)



app.include_router(movies.router)



