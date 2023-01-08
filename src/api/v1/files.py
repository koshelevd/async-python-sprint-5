import os

from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import FileResponse

from cache.cache import cached

from api.depends import get_current_user, get_file_service
from db.tables import User
from dto.files_schemas import FileEntity, UserDirsInfo, UserFilesList
from services import FileService
from services.exceptions import BaseSimpleException
from settings.storage import storage_settings

router = APIRouter()


# alias - str specifying the alias to load the config from
# /src/settings/cache/settings.py
@cached(ttl=10, alias="redis_alt")
@router.get(
    "/list", response_model=UserFilesList, summary="Get user's files info"
)
async def list(
    user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service),
):
    """Get info about user's files."""
    return await file_service.get_user_files(user)


@cached(ttl=10, alias="redis_alt")
@router.get(
    "/download",
    summary="Download file",
)
async def download_file(
    path: str,
    user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service),
):
    """Download file."""
    try:
        file = await file_service.get_user_file(path, user)
    except SQLAlchemyError as err:
        raise BaseSimpleException(
            message="Bad path parameter", context=str(err)
        )
    full_path = os.getcwd() + storage_settings.ROOT_DIR + file.path
    return FileResponse(
        path=full_path,
        media_type="application/octet-stream",
        filename=file.name,
    )


@router.post(
    "/upload",
    response_model=FileEntity,
    summary="Upload file to storage",
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(
    path: str,
    user: User = Depends(get_current_user),
    file: UploadFile = File(...),
    file_service: FileService = Depends(get_file_service),
):
    """Upload file to storage."""
    return await file_service.save_file_to_storage(path, file, user)


@cached(ttl=10, alias="redis_alt")
@router.get(
    "/user/status", response_model=UserDirsInfo, summary="Get user's dirs info"
)
async def status(
    user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service),
):
    """Get info about user's dirs."""
    return await file_service.get_dir_info(user)
