# src/api/app.py
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
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

app.include_router(api)
