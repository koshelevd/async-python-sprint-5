import json
import os

from fastapi import status


async def test_create_user(client, async_session):
    data = {"email": "testuser2@nofoobar.com", "password": "testing"}
    response = await client.post("/register", content=json.dumps(data))
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == "testuser2@nofoobar.com"


async def test_auth(client, user):
    data = {"username": user.email, "password": user.password}
    response = await client.post("/auth", data=data)
    assert response.status_code == status.HTTP_200_OK


async def test_upload_file(client, user):
    params = {"path": "/"}
    files = {"file": ("test.tst", open(os.getcwd() + "/tests/test.tst", "rb"))}
    response = await client.post(
        "/upload", params=params, files=files, headers=user.headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "test.tst"


async def test_get_user_files(client, user):
    response = await client.get("/list", headers=user.headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["files"][0]["name"] == "test.tst"
