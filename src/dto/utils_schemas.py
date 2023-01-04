from pydantic import Field

from dto.base import BaseSchema

_detail_ok_content = {
    "content": {"application/json": {"example": {"detail": "ok"}}}
}


class HandledExceptionSchema(BaseSchema):
    message: str
    description: str
    status: int
    context: dict = Field(
        example=[{"detail": "string"}, {"field_name": "field_error"}]
    )


class HandledValidationExceptionSchema(HandledExceptionSchema):
    context: list = Field(
        example=[
            [
                {
                    "loc": ["loc(body/query/nested/)", "field"],
                    "msg": "field required",
                    "type": "type_error.missing",
                }
            ]
        ]
    )
