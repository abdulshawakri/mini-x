from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from mini_x.infra.db.models.user import User
from mini_x.repositories.user.user_abc import UserRepositoryABC


class UserRepository(UserRepositoryABC):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_username(self, username: str) -> User | None:
        async with self._session.begin():
            result = await self._session.execute(
                select(User).filter(User.username == username)
            )
            return result.scalars().first()

    async def get_by_email(self, email: str) -> User | None:
        async with self._session.begin():
            result = await self._session.execute(
                select(User).filter(User.email == email)
            )
            return result.scalars().first()

    async def upsert(self, user: User) -> None:
        async with self._session.begin():
            await self._session.merge(user)
