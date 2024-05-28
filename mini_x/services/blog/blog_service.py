from uuid import UUID

from mini_x.api.v1.models.blog import (
    BlogPostCreate,
    BlogPostRead,
    BlogPostUpdate,
    BlogPostDelete,
)
from mini_x.repositories.blog.blog_abc import BlogRepositoryABC
from mini_x.services.blog.error import (
    BlogServiceException,
    BlogServiceUnAuthorizedException,
)
from mini_x.services.user.user_service import UserService


class BlogService:
    def __init__(
        self, blog_repository: BlogRepositoryABC, user_service: UserService
    ) -> None:
        self._blog_repository = blog_repository
        self._user_service = user_service

    async def create_post(
        self, post_data: BlogPostCreate, user_from_token: str
    ) -> BlogPostRead:
        current_user = await self._user_service.get_current_user(user_from_token)

        post = await self._blog_repository.create_post(
            current_user.id, post_data.content
        )
        return BlogPostRead.from_orm(post)

    async def get_post_by_id(self, post_id: UUID) -> BlogPostRead:
        post = await self._blog_repository.get_post_by_id(post_id)

        if post is None:
            raise BlogServiceException(f"Post {post_id} not found.")

        return BlogPostRead.from_orm(post)

    async def get_posts_by_user_id(
        self, user_id: UUID, offset: int = 0, limit: int = 10
    ):
        posts = await self._blog_repository.get_posts_by_user_id(user_id, offset, limit)
        return [BlogPostRead.from_orm(post) for post in posts]

    async def update_post(
        self, post_id: UUID, post_data: BlogPostUpdate, user_from_token: str
    ) -> BlogPostRead:
        current_user = await self._user_service.get_current_user(user_from_token)
        post = await self.get_post_by_id(post_id)

        if post.user_id != current_user.id:
            raise BlogServiceUnAuthorizedException(
                "Not authorized user to update this post"
            )

        updated_post = await self._blog_repository.update_post(
            post_id, post_data.content
        )

        if updated_post is None:
            raise BlogServiceException(f"Post {post_id} not found.")

        return BlogPostRead.from_orm(updated_post)

    async def delete_post(self, post_id: UUID, user_from_token: str) -> BlogPostDelete:
        current_user = await self._user_service.get_current_user(user_from_token)
        post = await self.get_post_by_id(post_id)

        if post.user_id != current_user.id:
            raise BlogServiceUnAuthorizedException(
                "Not authorized user to update this post"
            )

        await self._blog_repository.delete_post(post_id)
        return BlogPostDelete(post_id=post_id, message="Post successfully deleted")
