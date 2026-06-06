# src/api/app.py
import logging
import os
import asyncio
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import context
from src.api.services import TransitApi
from src.api.routers import api
from uvicorn.config import LOGGING_CONFIG
from uvicorn.logging import DefaultFormatter

load_dotenv()

handler = logging.StreamHandler()
handler.setFormatter(DefaultFormatter("%(asctime)s %(levelprefix)s %(message)s"))
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)
LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s %(levelprefix)s %(message)s"
LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with TransitApi() as api:
        context.transit_api = api
        context.load_available_stops()
        all_ids = ','.join(context.GLOBAL_STOP_ID_MAPPING.values())
        task = asyncio.create_task(context.departures_broadcaster.start(api, all_ids))
        yield
        task.cancel()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ["ORIGIN"]],
    allow_methods=["GET"],
)

app.include_router(api)
