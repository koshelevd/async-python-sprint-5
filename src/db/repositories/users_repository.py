from sqlalchemy import select

from db.repositories.base_repository import RepositoryBase
from db.tables import User


class UserRepository(RepositoryBase):
    """User repository"""

    model = User

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Get user by email.

        :param email: users email
        :return: user
        """

        query = select(User).filter_by(email=email)
        expr = await self.session.execute(query)
        return expr.scalar_one_or_none()
