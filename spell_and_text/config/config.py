import os

import aioredis
from aioredis import Redis
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


async def initiate_database() -> None:
    if os.getenv("ENVIRONMENT") == "local":
        client = AsyncIOMotorClient(os.getenv("LOCAL_DATABASE_URL"))
    else:
        client = AsyncIOMotorClient(os.getenv("DEV_DATABASE_URL"))
    await init_beanie(database=client.get_default_database(),
                      document_models=[])  # type: ignore


async def initiate_redis_pool() -> Redis:
    redis_connection = await aioredis.from_url(
        os.getenv("REDIS_AUTH_URL"),
        password=os.getenv("REDIS_PASSWORD"),
        encoding="utf-8",
        db=os.getenv("REDIS_USER_DB"),
        decode_responses=True,
    )
    return redis_connection
