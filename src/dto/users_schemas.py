from dto.base import BaseSchema, ORMBaseSchema


class BaseUserSchema(ORMBaseSchema):
    email: str


class UserDTO(BaseUserSchema):
    password: str


class UserResponseEntity(BaseUserSchema):
    id: int


class TokenSchema(BaseSchema):
    access_token: str
    refresh_token: str


class TokenPayload(BaseSchema):
    sub: str = None
    exp: int = None
