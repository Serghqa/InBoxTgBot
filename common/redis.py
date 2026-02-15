from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from redis.asyncio import Redis

from config import load_config, Config


config: Config = load_config()

redis = Redis(
    host=config.redis.HOST,
    port=config.redis.PORT,
    db=config.redis.DB,
)

redis_storage = RedisStorage(
    redis=redis,
    key_builder=DefaultKeyBuilder(with_destiny=True),
)
