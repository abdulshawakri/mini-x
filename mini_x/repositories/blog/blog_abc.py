import uuid
from abc import ABC, abstractmethod
from typing import Sequence

from mini_x.infra.db.models.blog import BlogPost


class BlogRepositoryABC(ABC):
    @abstractmethod
    async def create_post(self, user_id: uuid.UUID, content: str) -> BlogPost:
        raise NotImplementedError

    @abstractmethod
    async def get_post_by_id(self, post_id: uuid.UUID) -> BlogPost | None:
        raise NotImplementedError

    @abstractmethod
    async def get_posts_by_user_id(
        self, user_id: uuid.UUID, offset: int = 0, limit: int = 10
    ) -> Sequence[BlogPost]:
        raise NotImplementedError

    @abstractmethod
    async def update_post(self, post_id: uuid.UUID, content: str) -> BlogPost:
        raise NotImplementedError

    @abstractmethod
    async def delete_post(self, post_id: uuid.UUID) -> None:
        raise NotImplementedError
