from pydantic import BaseModel


class BaseSchema(BaseModel):
    ...


class ORMBaseSchema(BaseModel):
    class Config:
        orm_mode = True
