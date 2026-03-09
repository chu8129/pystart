# We want to revert this change: https://github.com/python/cpython/pull/1030
# Additional context is here: https://github.com/aio-libs/aiopg/issues/837
import selectors  # isort:skip # noqa: F401

selectors._PollLikeSelector.modify = (  # type: ignore
    selectors._BaseSelectorImpl.modify  # type: ignore
)  # noqa: E402

from dotenv import load_dotenv

load_dotenv()

import logging

from config.log import LOG_CONFIG

logging.basicConfig(
    level=getattr(logging, LOG_CONFIG["level"].upper()),
    format=LOG_CONFIG["format"],
    datefmt=LOG_CONFIG["date_format"],
)

from loguru import logger

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

from model.enviroment import Environment
from model.memory import MemoryMetric
from provider.database import db
from router.enviroment import router as env_router
from router.memory import router as memory_router
from utils.env_loader import load_env_from_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Application starting...")

    db.create_tables([MemoryMetric, Environment], safe=True)

    logger.info(f"Loaded {load_env_from_db()} environment variables from database to system environment")

    yield

    logger.info("Application shutting down...")


API_CONFIG = {"title": "qw", "version": "0.01", "description": ""}

app = FastAPI(**API_CONFIG, lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


app.include_router(memory_router)
app.include_router(env_router)
