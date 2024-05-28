import uuid
from unittest.mock import Mock

import pytest

from mini_x.api.v1.models.blog import BlogPostCreate, BlogPostUpdate
from mini_x.infra.db.models.blog import BlogPost
from mini_x.services.blog.blog_service import BlogService
from mini_x.services.blog.error import BlogServiceException


@pytest.fixture
def blog_service(mock_blog_repo: Mock) -> BlogService:
    return BlogService(blog_repository=mock_blog_repo)


@pytest.mark.asyncio
async def test_create_post(blog_service: BlogService, mock_blog_repo: Mock) -> None:
    user_id = uuid.uuid4()
    post_data = BlogPostCreate(content="Test content")

    blog_post = BlogPost(
        id=uuid.uuid4(),
        user_id=user_id,
        content=post_data.content,
    )

    mock_blog_repo.create_post.return_value = blog_post

    created_post = await blog_service.create_post(user_id, post_data)

    assert created_post.content == post_data.content
    assert created_post.user_id == user_id


@pytest.mark.asyncio
async def test_get_post_by_id(blog_service: BlogService, mock_blog_repo: Mock) -> None:
    post_id = uuid.uuid4()
    blog_post = BlogPost(
        id=post_id,
        user_id=uuid.uuid4(),
        content="Test content",
    )

    mock_blog_repo.get_post_by_id.return_value = blog_post

    retrieved_post = await blog_service.get_post_by_id(post_id)

    assert retrieved_post.id == post_id
    assert retrieved_post.content == blog_post.content


@pytest.mark.asyncio
async def test_get_post_by_id_not_found(
    blog_service: BlogService, mock_blog_repo: Mock
) -> None:
    post_id = uuid.uuid4()

    mock_blog_repo.get_post_by_id.return_value = None

    with pytest.raises(BlogServiceException):
        await blog_service.get_post_by_id(post_id)


@pytest.mark.asyncio
async def test_get_posts_by_user_id(
    blog_service: BlogService, mock_blog_repo: Mock
) -> None:
    user_id = uuid.uuid4()
    blog_posts = [
        BlogPost(id=uuid.uuid4(), user_id=user_id, content="Test content 1"),
        BlogPost(id=uuid.uuid4(), user_id=user_id, content="Test content 2"),
    ]

    mock_blog_repo.get_posts_by_user_id.return_value = blog_posts

    retrieved_posts = await blog_service.get_posts_by_user_id(user_id)

    assert len(retrieved_posts) == 2
    assert retrieved_posts[0].content == blog_posts[0].content
    assert retrieved_posts[1].content == blog_posts[1].content


@pytest.mark.asyncio
async def test_update_post(blog_service: BlogService, mock_blog_repo: Mock) -> None:
    post_id = uuid.uuid4()
    post_data = BlogPostUpdate(content="Updated content")
    blog_post = BlogPost(
        id=post_id,
        user_id=uuid.uuid4(),
        content=post_data.content,
    )

    mock_blog_repo.update_post.return_value = blog_post

    updated_post = await blog_service.update_post(post_id, post_data)

    assert updated_post.content == post_data.content


@pytest.mark.asyncio
async def test_update_post_not_found(
    blog_service: BlogService, mock_blog_repo: Mock
) -> None:
    post_id = uuid.uuid4()
    post_data = BlogPostUpdate(content="Updated content")

    mock_blog_repo.update_post.return_value = None

    with pytest.raises(BlogServiceException):
        await blog_service.update_post(post_id, post_data)


@pytest.mark.asyncio
async def test_delete_post(blog_service: BlogService, mock_blog_repo: Mock) -> None:
    post_id = uuid.uuid4()

    await blog_service.delete_post(post_id)

    mock_blog_repo.delete_post.assert_called_once_with(post_id)
