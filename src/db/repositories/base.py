from abc import ABC, abstractmethod

from anyio import Any
from sqlalchemy.ext.asyncio import AsyncSession

from db.tables.base import BaseModel


class BaseRepository(ABC):
    """
    Repository base class.

    Repository never commits. It's up to the layer using this repo to decide
    when to commit. This allows for the layer to use repos's methods
    and manage transaction itself.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def is_exists(self, **kwargs):
        ...

    async def validate_uniques(self, obj: BaseModel) -> list[str]:
        exc_context = []
        for column in obj.__table__.columns:
            if column.unique and not column.name == "id":
                to_search = {column.name: getattr(obj, column.name)}
                if await self.is_exists(**to_search):
                    exc_context.append(column.name)

        return exc_context

    async def validate_uniques_by_values(
        self, model: type[BaseModel], obj_data: dict[str, Any]
    ) -> list[str]:
        exc_context = []
        unique_columns = [
            column.name for column in model.__table__.columns if column.unique
        ]
        for column, value in obj_data.items():
            if column in unique_columns and await self.is_exists(
                **{column: value}
            ):
                exc_context.append(column)
        return exc_context
