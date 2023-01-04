from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException

from dto.utils_schemas import (
    HandledExceptionSchema,
    HandledValidationExceptionSchema,
)
from services.exceptions import BaseCustomException, BaseFieldException
from utils.basic_logg import logg


async def base_exception_handler(request: Request, exc: BaseCustomException):
    exception_schema = HandledExceptionSchema(
        description=exc.description,
        status=exc.status,
        message=exc.message,
        context=exc.context
        if isinstance(exc, BaseFieldException)
        else {"detail": exc.context},
    )
    return JSONResponse(
        status_code=exc.status, content=exception_schema.dict()
    )


async def http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:  # noqa
    exception_schema = HandledExceptionSchema(
        description="",
        status=exc.status_code,
        message="",
        context={"detail": exc.detail},
    )
    return JSONResponse(
        status_code=exc.status_code, content=exception_schema.dict()
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:  # noqa
    exception_schema = HandledValidationExceptionSchema(
        description="Unprocessable Entity",
        status=422,
        message="Unable to process request's body/params",
        context=jsonable_encoder(exc.errors()),
    )
    return JSONResponse(
        status_code=exception_schema.status, content=exception_schema.dict()
    )


async def sqlalchemy_exception_handler(request: Request, exc: IntegrityError):
    logg.exception("DB error")
    exception_schema = HandledExceptionSchema(
        description="Internal Server Error",
        status=500,
        message="",
        context={"detail": None},
    )
    return JSONResponse(status_code=500, content=exception_schema.dict())
