import json
import os

import pytest
from fastapi import status


class User:
    def __init__(self, token):
        self.token = token
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def set_token(self, token):
        self.token = token
        self.headers = {"Authorization": f"Bearer {self.token}"}


user = User(None)


@pytest.mark.asyncio
async def test_create_user(client, async_session):
    data = {"email": "testuser@nofoobar.com", "password": "testing"}
    response = await client.post("/register", content=json.dumps(data))
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == "testuser@nofoobar.com"


@pytest.mark.asyncio
async def test_auth(client, async_session):
    data = {"username": "testuser@nofoobar.com", "password": "testing"}
    response = await client.post("/auth", data=data)
    assert response.status_code == status.HTTP_200_OK
    token = response.json().get("access_token")
    user.set_token(token)


@pytest.mark.asyncio
async def test_upload_file(client, async_session):
    params = {"path": "/"}
    files = {"file": ("test.tst", open(os.getcwd() + "/tests/test.tst", "rb"))}
    response = await client.post(
        "/upload", params=params, files=files, headers=user.headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "test.tst"


@pytest.mark.asyncio
async def test_get_user_files(client, async_session):
    response = await client.get("/list", headers=user.headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["files"][0]["name"] == "test.tst"
