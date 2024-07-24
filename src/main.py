import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_scheduler import SchedulerAdmin
from loguru import logger
from redis import asyncio as aioredis

from config import settings
from parse_data.add_data import AddDataToDataBase
from parse_data.parse_data import ParseDataFromSite
from src.api import router
from src.metadata import DESCRIPTION, TAG_METADATA, TITLE, VERSION

site = AdminSite(settings=Settings(database_url_async=settings.DB_URL_SCHEDULER))
scheduler = SchedulerAdmin.bind(site)


@scheduler.scheduled_job(trigger="cron", hour=19, minute=11)
def clear_cache():
    FastAPICache.clear()
    logger.info("Cache delete!")


async def start_parse():
    parse = ParseDataFromSite()
    add_data_class = AddDataToDataBase()
    await parse.get_page_count()
    await add_data_class.add_processing_data_to_db()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    logger.info("Start redis cache")
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf-8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    scheduler.start()
    await start_parse()
    yield
    await redis.close()
    logger.info("Shutdown redis cache")


def create_fastapi_app():
    load_dotenv(find_dotenv(".env"))
    env_name = os.getenv("MODE", "DEV")

    if env_name != "PROD":
        _app = FastAPI(
            default_response_class=ORJSONResponse,
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            openapi_tags=TAG_METADATA,
            lifespan=lifespan,
        )
    else:
        _app = FastAPI(
            default_response_class=ORJSONResponse,
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            openapi_tags=TAG_METADATA,
            lifespan=lifespan,
            docs_url=None,
            redoc_url=None,
        )

    _app.include_router(router, prefix="/api")
    return _app


app = create_fastapi_app()

site.mount_app(app)
