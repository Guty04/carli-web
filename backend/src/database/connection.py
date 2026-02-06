from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.configurations import configuration
from src.enums import Environment


class Database:
    def __init__(self) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=configuration.DATABASE_URL.encoded_string(),
            echo=configuration.ENVIRONMENT == Environment.DEVELOPMENT,
            pool_size=10,
        )
        self.session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )

    async def get_async_session(self) -> AsyncGenerator[AsyncSession]:
        async with self.session_maker() as session:
            try:
                yield session
                await session.commit()

            except Exception:
                await session.rollback()
                raise

            finally:
                await session.close()


database: Database = Database()
