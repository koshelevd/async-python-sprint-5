from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


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
