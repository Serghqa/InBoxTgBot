from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)

# from db import Base
from config import load_config, Config


config: Config = load_config()


def create_engine(config: Config) -> AsyncEngine:

    engine: AsyncEngine = create_async_engine(
        url=(
            f'postgresql+asyncpg://'
            f'{config.db.DB_USER}:{config.db.DB_PASSWORD}@'
            f'{config.db.DB_HOST}/{config.db.DB_NAME}'
        ),
        echo=False,
    )

    return engine


def create_async_sessionmaker(engine: AsyncEngine) -> async_sessionmaker:

    return async_sessionmaker(bind=engine, expire_on_commit=False)


# async def create_tables(engine: AsyncEngine):

#     async with engine.begin() as conn:
#         #  await conn.run_sync(Base.metadata.drop_all)  # для теста
#         await conn.run_sync(Base.metadata.create_all, checkfirst=True)


engine: AsyncEngine = create_engine(config)
Session = create_async_sessionmaker(engine)
