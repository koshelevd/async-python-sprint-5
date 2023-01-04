import logging.config

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from api.exception_handlers import (
    base_exception_handler,
    http_exception_handler,
    sqlalchemy_exception_handler,
    validation_exception_handler,
)
from api.v1 import router_v1
from db.tables import *  # noqa
from dto.utils_schemas import HandledValidationExceptionSchema
from services.exceptions import BaseCustomException
from settings.api import api_settings
from utils.logger_config import log_config


def _initialize_routers(app: FastAPI) -> None:
    app.include_router(router_v1, prefix="/api")


def _initialize_exception_handlers(app: FastAPI) -> None:
    del app.exception_handlers[RequestValidationError]

    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(
        RequestValidationError, validation_exception_handler
    )
    app.add_exception_handler(BaseCustomException, base_exception_handler)
    app.add_exception_handler(IntegrityError, sqlalchemy_exception_handler)


def initialize_app() -> FastAPI:
    app = FastAPI(
        title=api_settings.PROJECT_NAME,
        responses={
            422: {
                "description": "Validation Error",
                "model": HandledValidationExceptionSchema,
            }
        },
    )
    # logging.config.dictConfig(log_config)
    _initialize_routers(app)
    _initialize_exception_handlers(app)
    return app
