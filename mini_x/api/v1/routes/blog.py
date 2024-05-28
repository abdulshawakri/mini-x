from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query

from mini_x.api.v1.dependancies import (
    get_current_user_from_token,
    get_blog_service,
    get_user_service,
)
from mini_x.api.v1.models.blog import (
    BlogPostRead,
    BlogPostUpdate,
    BlogPostCreate,
    BlogPostDelete,
)
from mini_x.services.blog.blog_service import BlogService
from mini_x.services.user.user_service import UserService

router = APIRouter()


@router.post(
    "/posts/", response_model=BlogPostRead, status_code=status.HTTP_201_CREATED
)
async def create_post(
    post_data: BlogPostCreate,
    user_from_token: Annotated[str, Depends(get_current_user_from_token)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    blog_service: Annotated[BlogService, Depends(get_blog_service)],
):
    try:
        current_user = await user_service.get_current_user(user_from_token)
        return await blog_service.create_post(
            user_id=current_user.id, post_data=post_data
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/posts/{post_id}", response_model=BlogPostRead)
async def update_post(
    post_id: UUID,
    post_data: BlogPostUpdate,
    user_from_token: Annotated[str, Depends(get_current_user_from_token)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    blog_service: Annotated[BlogService, Depends(get_blog_service)],
):
    try:
        current_user = await user_service.get_current_user(user_from_token)
        post = await blog_service.get_post_by_id(post_id)
        if post.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this post",
            )
        return await blog_service.update_post(post_id, post_data=post_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: UUID,
    user_from_token: Annotated[str, Depends(get_current_user_from_token)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    blog_service: Annotated[BlogService, Depends(get_blog_service)],
) -> BlogPostDelete:
    try:
        current_user = await user_service.get_current_user(user_from_token)
        post = await blog_service.get_post_by_id(post_id)
        if post.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this post",
            )
        await blog_service.delete_post(post_id)
        return BlogPostDelete(post_id=post_id, message="Post successfully deleted")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# In these routs provide the APIs to be publicly available for the internet.
@router.get("/posts/{post_id}")
async def read_post(
    post_id: UUID, blog_service: BlogService = Depends(get_blog_service)
) -> BlogPostRead:
    try:
        return await blog_service.get_post_by_id(post_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/users/{user_id}/posts")
async def read_posts_by_user(
    user_id: UUID,
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    blog_service: BlogService = Depends(get_blog_service),
) -> list[BlogPostRead]:
    try:
        return await blog_service.get_posts_by_user_id(user_id, offset, limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
