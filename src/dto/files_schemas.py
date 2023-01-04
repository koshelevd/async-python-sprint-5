import uuid
from datetime import datetime

from dto.base import BaseSchema, ORMBaseSchema


class BaseFileSchema(ORMBaseSchema):
    name: str
    created_at: datetime
    path: str
    size: int
    is_downloadable: bool


class FileUploadDTO(ORMBaseSchema):
    path: str


class FileEntity(BaseFileSchema):
    id: uuid.UUID


class UserFilesList(ORMBaseSchema):
    account_id: uuid.UUID
    files: list[FileEntity]


class DirInfo(BaseSchema):
    used: int
    files: int


class Folders(BaseSchema):
    __root__: dict[str, DirInfo]


class UserDirsInfo(ORMBaseSchema):
    account_id: uuid.UUID
    folders: Folders


class PingStatus(BaseSchema):
    status: str = "OK"
    ping_db_time: float
