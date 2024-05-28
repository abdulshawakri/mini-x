from uuid import UUID

from mini_x.api.v1.models.blog import BlogPostCreate, BlogPostRead, BlogPostUpdate
from mini_x.repositories.blog.blog_abc import BlogRepositoryABC
from mini_x.services.blog.error import BlogServiceException


class BlogService:
    def __init__(self, blog_repository: BlogRepositoryABC):
        self.blog_repository = blog_repository

    async def create_post(
        self, user_id: UUID, post_data: BlogPostCreate
    ) -> BlogPostRead:
        post = await self.blog_repository.create_post(user_id, post_data.content)
        return BlogPostRead.from_orm(post)

    async def get_post_by_id(self, post_id: UUID) -> BlogPostRead:
        post = await self.blog_repository.get_post_by_id(post_id)

        if post is None:
            raise BlogServiceException(f"Post {post_id} not found.")

        return BlogPostRead.from_orm(post)

    async def get_posts_by_user_id(
        self, user_id: UUID, offset: int = 0, limit: int = 10
    ):
        posts = await self.blog_repository.get_posts_by_user_id(user_id, offset, limit)
        return [BlogPostRead.from_orm(post) for post in posts]

    async def update_post(
        self, post_id: UUID, post_data: BlogPostUpdate
    ) -> BlogPostRead:
        post = await self.blog_repository.update_post(post_id, post_data.content)

        if post is None:
            raise BlogServiceException(f"Post {post_id} not found.")

        return BlogPostRead.from_orm(post)

    async def delete_post(self, post_id: UUID) -> None:
        await self.blog_repository.delete_post(post_id)
