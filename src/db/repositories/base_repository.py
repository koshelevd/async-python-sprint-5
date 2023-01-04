import uuid
from datetime import datetime

from sqlalchemy import asc, delete, desc, select, update

from db.repositories.base import BaseRepository
from db.tables.base import BaseModel
from utils.const import type_sorted_asc, type_sorted_desc


class RepositoryBase(BaseRepository):
    """Repository class with basic CRUD operations."""

    model = BaseModel

    async def is_exists(self, **kwargs):
        query = select(select(self.model.id).filter_by(**kwargs).exists())
        obj = await self.session.execute(query)
        return obj.scalar()

    async def get_by_id(self, obj_id: uuid.UUID) -> model:
        query = select(self.model).filter(self.model.id == obj_id)
        obj = await self.session.execute(query)
        return obj.scalar_one_or_none()

    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
        field_sorted: str = None,
        type_sorted: str = type_sorted_asc,
        **kwargs,
    ) -> list[model]:
        query = select(self.model).filter_by(is_deleted=False, **kwargs)
        if field_sorted is not None:
            if type_sorted == type_sorted_desc:
                query = query.order_by(desc(field_sorted))
            else:
                query = query.order_by(asc(field_sorted))
        query = query.limit(limit).offset(offset)

        obj = await self.session.execute(query)
        return obj.scalars().all()

    async def update(self, obj_id: int, **kwargs) -> None:
        query = (
            update(self.model).values(**kwargs).filter(self.model.id == obj_id)
        )
        await self.session.execute(query)
        return None

    async def delete(self, obj_id: int) -> None:
        query = (
            update(self.model)
            .filter(self.model.id == obj_id)
            .values(is_deleted=True, deleted_at=datetime.now())
        )
        await self.session.execute(query)
        return None

    async def delete_force(self, obj_id: int) -> None:
        query = delete(self.model).filter(self.model.id == obj_id)
        await self.session.execute(query)
        return None

    def create(self, *args, **kwargs) -> model:
        obj = self.model(*args, **kwargs)
        return obj
