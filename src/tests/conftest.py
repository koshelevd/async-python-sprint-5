import asyncio
import json
from typing import AsyncGenerator, Generator

import asyncpg
import pytest
import pytest_asyncio
from fastapi import Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from api.depends import get_user_service
from db.utils.db_session import Base, engine
from settings.app import initialize_app

BASE_URL = "http://127.0.0.1/api/v1"


class TestUser:
    def __init__(self, email: str, password: str, token: str):
        self.email = email
        self.password = password
        self.token = token
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def set_token(self, token):
        self.token = token
        self.headers = {"Authorization": f"Bearer {self.token}"}


@pytest_asyncio.fixture(scope="function")
async def user(async_session: AsyncSession, client: AsyncClient) -> TestUser:
    data = {"email": "testuser@nofoobar.com", "password": "testing"}
    await client.post("/register", content=json.dumps(data))
    response = await client.post(
        "/auth", data={"username": data["email"], "password": data["password"]}
    )
    token = response.json().get("access_token")
    return TestUser(data["email"], data["password"], token)


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
