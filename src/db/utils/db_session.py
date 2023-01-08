from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from settings.db import db_settings

Base = declarative_base()

engine = create_async_engine(
    db_settings.get_db_url(),
    echo=True,
)
Session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession, future=True
)


async def get_session() -> AsyncGenerator:
    session = Session()
    try:
        yield session
        # коммиты и ролбэки обрабатываем в сервисах
    finally:
        await session.close()
