from fastapi import APIRouter

from api.v1.common import router as common_router
from api.v1.files import router as files_router
from api.v1.users import router as auth_router

router_v1 = APIRouter(prefix="/v1")

router_v1.include_router(common_router, tags=["common"])
router_v1.include_router(auth_router, tags=["user"])
router_v1.include_router(files_router, tags=["storage"])
