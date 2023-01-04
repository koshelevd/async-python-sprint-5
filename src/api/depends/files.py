from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories import FileRepository
from db.utils.db_session import get_session
from services import FileService


async def get_file_repository(
    session: AsyncSession = Depends(get_session),
) -> FileRepository:
    return FileRepository(session)


async def get_file_service(
    repository: FileRepository = Depends(get_file_repository),
) -> FileService:
    return FileService(file_repository=repository)
