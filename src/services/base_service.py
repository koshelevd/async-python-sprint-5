from db.repositories.base_repository import RepositoryBase
from db.tables.base import BaseModel
from services.exceptions import (
    NotFoundValueException,
    UniqueValidationException,
)
from utils.const import type_sorted_asc


class BaseService:
    """
    BaseService is a class that contains the basic
    CRUD operations for the repository.
    """

    model: BaseModel = None

    def __init__(self, obj_repo: RepositoryBase):
        self.obj_repo = obj_repo

    async def get(self, id: int) -> model:
        obj = await self.obj_repo.get_by_id(id)
        if not obj:
            raise NotFoundValueException(["id"])
        return obj

    async def get_all(
        self,
        limit: int | None = 100,
        offset: int = 0,
        field_sorted: str = None,
        type_sorted: str = type_sorted_asc,
        **kwargs,
    ) -> list[model]:
        if field_sorted is not None:
            if self.model.__dict__.get(field_sorted, None) is None:
                raise NotFoundValueException(["field_sorted"])
        examples = await self.obj_repo.get_all(
            limit=limit,
            offset=offset,
            field_sorted=field_sorted,
            type_sorted=type_sorted,
            **kwargs,
        )
        return examples

    async def create(self, **kwargs) -> model:
        obj = self.obj_repo.create(**kwargs)
        unique_fields_exceptions = await self.obj_repo.validate_uniques(obj)
        if unique_fields_exceptions:
            raise UniqueValidationException(unique_fields_exceptions)

        self.obj_repo.session.add(obj)
        await self.obj_repo.session.commit()
        return obj

    async def update(self, id, **kwargs) -> model:
        if not await self.obj_repo.is_exists(id=id):
            raise NotFoundValueException(["id"])
        to_update = {}
        for item in kwargs:
            if kwargs[item] is not None:
                to_update[item] = kwargs[item]
        unique_fields_exceptions = (
            await self.obj_repo.validate_uniques_by_values(
                self.model, to_update
            )
        )
        if unique_fields_exceptions:
            raise UniqueValidationException(unique_fields_exceptions)

        await self.obj_repo.update(id, **to_update)
        await self.obj_repo.session.commit()

        obj = await self.obj_repo.get_by_id(id)
        return obj

    async def delete(self, id: int) -> None:
        if not await self.obj_repo.is_exists(id=id):
            raise NotFoundValueException(["id"])
        await self.obj_repo.delete(id)
        await self.obj_repo.session.commit()
        return None

    async def delete_force(self, id: int) -> None:
        if not await self.obj_repo.is_exists(id=id):
            raise NotFoundValueException(["id"])
        await self.obj_repo.delete_force(id)
        await self.obj_repo.session.commit()
        return None
