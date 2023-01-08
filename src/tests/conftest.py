import asyncio
from typing import AsyncGenerator, Generator

import asyncpg
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from db.utils.db_session import Base, engine
from settings.app import initialize_app

BASE_URL = "http://127.0.0.1/api/v1"


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncGenerator:
    async with AsyncClient(app=initialize_app(), base_url=BASE_URL) as client:
        yield client


@pytest_asyncio.fixture(scope="module")
async def async_session() -> AsyncGenerator:
    session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    await _connect_db(user="postgres", database="test_db", password="postgres")
    async with session() as s:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield s
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


async def _connect_db(user, database, password):
    try:
        conn = await asyncpg.connect(
            user=user,
            database=database,
            password=password,
            max_cached_statement_lifetime=6,
            host="127.0.0.1",
            port=5432,
        )
    except asyncpg.InvalidCatalogNameError:
        sys_conn = await asyncpg.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            host="127.0.0.1",
            port=5432,
        )
        await sys_conn.execute(f'CREATE DATABASE "{database}" OWNER "{user}"')
        await sys_conn.close()
        conn = await asyncpg.connect(
            user=user,
            database=database,
            password=password,
            host="127.0.0.1",
            port=5432,
        )
    return conn
