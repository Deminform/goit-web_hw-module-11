import contextlib

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from conf.config import db_config


class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(autocommit=False, autoflush=False,
                                                                     bind=self._engine)

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception('Session maker not defined')
        session = self._session_maker()
        try:
            yield session
        except SQLAlchemyError as error:
            print(error)
            await session.rollback()
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(db_config.DB_URL)


async def get_db():
    async with sessionmanager.session() as session:
        yield session
