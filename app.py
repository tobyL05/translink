# src/api/app.py
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import context
from src.api.services import TransitApi
from src.api.routers import api

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with TransitApi() as api:
        context.transit_api = api
        context.load_available_stops()
        yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ["ORIGIN"] ],
    allow_methods=["GET"],
)

app.include_router(api)
