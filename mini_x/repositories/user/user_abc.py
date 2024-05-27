from abc import ABC, abstractmethod

from mini_x.infra.db.models.user import User


class UserRepositoryABC(ABC):
    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def upsert(self, user: User) -> None:
        raise NotImplementedError
