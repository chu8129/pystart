import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.memory import router as memory_router
from config.database import API_CONFIG
from model.memory import MemoryMetric
from providers.database import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Application starting...")
    # db.create_tables([MemoryMetric], safe=True)
    yield
    logger.info("Application shutting down...")

app = FastAPI(
    **API_CONFIG,
    lifespan=lifespan
)

app.include_router(memory_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)