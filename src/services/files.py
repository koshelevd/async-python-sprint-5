import os.path
import time
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.exc import SQLAlchemyError

from db.repositories import FileRepository
from db.tables import File, User
from dto.files_schemas import PingStatus, UserDirsInfo, UserFilesList
from services.exceptions import NotAuthorizedException, NotFoundValueException
from settings.storage import storage_settings


class FileService:
    """Service for working with file storage."""

    def __init__(self, *, file_repository: FileRepository):
        self.file_repo = file_repository

    async def get_dir_info(self, user):
        files = await self.file_repo.get_user_files(user)
        result = {}
        for file in files:
            folder = os.path.dirname(file.path)
            full_path = os.getcwd() + storage_settings.ROOT_DIR + file.path
            file_size = os.path.getsize(full_path)
            if result.get(folder) is None:
                result[folder] = {"used": 0, "files": 0}
            result[folder] = {
                "used": result[folder]["used"] + file_size,
                "files": result[folder]["files"] + 1,
            }
        return UserDirsInfo(account_id=user.id, folders=result)

    async def ping(self):
        """Check service DB availability."""
        try:
            start_db_time = time.time()
            await self.file_repo.ping()
            ping_db_time = time.time() - start_db_time
        except SQLAlchemyError:
            raise
        return PingStatus(ping_db_time=ping_db_time)

    async def get_user_file(self, path: str, user: User) -> File:
        if path.startswith("/"):
            file = await self.file_repo.get_user_file_by_path(path, user)
        else:
            file = await self.file_repo.get_by_id(obj_id=path)

        if file is None:
            raise NotFoundValueException(fields=["path"])
        if file.user != user:
            raise NotAuthorizedException(
                context="File belongs to another user"
            )

        return file

    async def get_user_files(self, user: User) -> UserFilesList:
        files = await self.file_repo.get_user_files(user)
        result = UserFilesList(account_id=user.id, files=files)
        return result

    async def save_file_to_storage(
        self, path: str, file: UploadFile, user: User
    ) -> File:
        filename = ""
        if not path.startswith("/"):
            filename = "/"
        if path.endswith("/"):
            filename += path + file.filename
        else:
            filename += path
        full_path = os.getcwd() + storage_settings.ROOT_DIR + filename
        existing_file = await self.file_repo.get_by_filename(
            os.path.basename(filename)
        )
        if existing_file and existing_file.user != user:
            raise NotAuthorizedException(
                context="File exists and belongs to another user"
            )
        size = await self._save_file_to_storage(full_path=full_path, file=file)
        if existing_file:
            saved_file = await self.file_repo.update(
                obj_id=existing_file.id, size=size
            )
        else:
            saved_file = self.file_repo.create(
                name=os.path.basename(filename),
                path=filename,
                size=size,
                user=user,
            )
            self.file_repo.session.add(saved_file)

        try:
            await self.file_repo.session.commit()
        except SQLAlchemyError:
            await self.file_repo.session.rollback()
            raise

        if saved_file is None:
            saved_file = await self.file_repo.get_by_id(existing_file.id)

        return saved_file

    @staticmethod
    async def _save_file_to_storage(full_path: str, file: UploadFile):
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "wb") as file_to_save:
                content = await file.read()
                file_to_save.write(content)
                file_to_save.close()
        except OSError as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err),
            )
        size = os.path.getsize(full_path)
        return size
