from sqlalchemy import select

from db.repositories.base_repository import RepositoryBase
from db.tables import File, User


class FileRepository(RepositoryBase):
    """File storage repository."""

    model = File

    async def ping(self) -> bool:
        """Ping DB."""
        query = select(1)
        expr = await self.session.execute(query)
        return bool(expr.scalars().all())

    async def get_by_filename(self, filename: str) -> File | None:
        query = select(File).filter(File.name == filename)
        expr = await self.session.execute(query)
        return expr.scalar_one_or_none()

    async def get_user_file_by_path(
        self, path: str, user: User
    ) -> File | None:
        query = select(File).filter(File.path == path, File.user == user)
        expr = await self.session.execute(query)
        return expr.scalar_one_or_none()

    async def get_user_files(self, user: User) -> list[File]:
        query = select(File).filter(File.user == user)
        expr = await self.session.execute(query)
        return expr.scalars().all()
