from fastapi import APIRouter, Depends

from api.depends import get_file_service
from dto.files_schemas import PingStatus
from services import FileService

router = APIRouter()


@router.get(
    "/ping", summary="Check service DB availability", response_model=PingStatus
)
async def ping(file_service: FileService = Depends(get_file_service)):
    """Check service DB availability."""
    return await file_service.ping()
