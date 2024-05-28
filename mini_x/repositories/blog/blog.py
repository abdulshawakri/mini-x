import uuid
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from mini_x.infra.db.models.blog import BlogPost
from repositories.blog.blog_abc import BlogRepositoryABC


class BlogRepository(BlogRepositoryABC):
    def __init__(self, db_session: AsyncSession):
        self._session = db_session

    async def create_post(self, user_id: uuid.UUID, content: str) -> BlogPost:
        post = BlogPost(user_id=user_id, content=content)

        async with self._session.begin():
            self._session.add(post)
            return post

    async def get_post_by_id(self, post_id: uuid.UUID) -> BlogPost | None:
        async with self._session.begin():
            result = await self._session.execute(
                select(BlogPost)
                .where(BlogPost.id == post_id)
                .options(selectinload(BlogPost.author))
            )
            return result.scalars().first()

    async def get_posts_by_user_id(
        self, user_id: uuid.UUID, offset: int = 0, limit: int = 10
    ) -> Sequence[BlogPost]:
        async with self._session.begin():
            result = await self._session.execute(
                select(BlogPost)
                .where(BlogPost.user_id == user_id)
                .options(selectinload(BlogPost.author))
                .offset(offset)
                .limit(limit)
            )
            return result.scalars().all()

    async def update_post(self, post_id: uuid.UUID, content: str) -> BlogPost | None:
        async with self._session.begin():
            post = await self._get_post_by_id(post_id)

            if post:
                post.content = content  # type: ignore[assignment]
                await self._session.merge(post)
            return post

    async def delete_post(self, post_id: uuid.UUID) -> None:
        async with self._session.begin():
            post = await self._get_post_by_id(post_id)

            if post:
                await self._session.delete(post)

    async def _get_post_by_id(self, post_id: uuid.UUID) -> BlogPost | None:
        result = await self._session.execute(
            select(BlogPost).where(BlogPost.id == post_id)
        )
        post = result.scalars().first()
        return post
