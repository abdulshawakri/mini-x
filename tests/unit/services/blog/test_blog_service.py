import uuid
from unittest.mock import Mock, AsyncMock

import pytest

from mini_x.api.v1.models.blog import BlogPostCreate, BlogPostUpdate
from mini_x.infra.db.models.blog import BlogPost
from mini_x.services.blog.blog_service import BlogService
from mini_x.services.blog.error import (
    BlogServiceException,
    BlogServiceUnAuthorizedException,
)


@pytest.fixture
def mock_user_service() -> Mock:
    return AsyncMock()


@pytest.fixture
def blog_service(mock_blog_repo: Mock, mock_user_service: Mock) -> BlogService:
    return BlogService(blog_repository=mock_blog_repo, user_service=mock_user_service)


@pytest.mark.asyncio
async def test_create_post(
    blog_service: BlogService, mock_blog_repo: Mock, mock_user_service: Mock
) -> None:
    user_id = uuid.uuid4()
    post_data = BlogPostCreate(content="Test content")
    user_token = "test_token"
    current_user = Mock(id=user_id)

    blog_post = BlogPost(
        id=uuid.uuid4(),
        user_id=user_id,
        content=post_data.content,
    )

    mock_user_service.get_current_user.return_value = current_user
    mock_blog_repo.create_post.return_value = blog_post

    created_post = await blog_service.create_post(post_data, user_token)

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
async def test_update_post(
    blog_service: BlogService, mock_blog_repo: Mock, mock_user_service: Mock
) -> None:
    post_id = uuid.uuid4()
    post_data = BlogPostUpdate(content="Updated content")
    user_token = "test_token"
    user_id = uuid.uuid4()
    current_user = Mock(id=user_id)
    blog_post = BlogPost(
        id=post_id,
        user_id=user_id,
        content="Original content",
    )
    updated_blog_post = BlogPost(
        id=post_id,
        user_id=user_id,
        content=post_data.content,
    )

    mock_user_service.get_current_user.return_value = current_user
    mock_blog_repo.get_post_by_id.return_value = blog_post
    mock_blog_repo.update_post.return_value = updated_blog_post

    updated_post = await blog_service.update_post(post_id, post_data, user_token)

    assert updated_post.content == post_data.content


@pytest.mark.asyncio
async def test_update_post_not_found(
    blog_service: BlogService, mock_blog_repo: Mock, mock_user_service: Mock
) -> None:
    post_id = uuid.uuid4()
    post_data = BlogPostUpdate(content="Updated content")
    user_token = "test_token"
    user_id = uuid.uuid4()
    current_user = Mock(id=user_id)

    mock_user_service.get_current_user.return_value = current_user
    mock_blog_repo.get_post_by_id.return_value = None

    with pytest.raises(BlogServiceException):
        await blog_service.update_post(post_id, post_data, user_token)


@pytest.mark.asyncio
async def test_update_post_unauthorized(
    blog_service: BlogService, mock_blog_repo: Mock, mock_user_service: Mock
) -> None:
    post_id = uuid.uuid4()
    post_data = BlogPostUpdate(content="Updated content")
    user_token = "test_token"
    user_id = uuid.uuid4()
    different_user_id = uuid.uuid4()
    current_user = Mock(id=user_id)
    blog_post = BlogPost(
        id=post_id,
        user_id=different_user_id,
        content="Original content",
    )

    mock_user_service.get_current_user.return_value = current_user
    mock_blog_repo.get_post_by_id.return_value = blog_post

    with pytest.raises(BlogServiceUnAuthorizedException):
        await blog_service.update_post(post_id, post_data, user_token)


@pytest.mark.asyncio
async def test_delete_post(
    blog_service: BlogService, mock_blog_repo: Mock, mock_user_service: Mock
) -> None:
    post_id = uuid.uuid4()
    user_token = "test_token"
    user_id = uuid.uuid4()
    current_user = Mock(id=user_id)
    blog_post = BlogPost(
        id=post_id,
        user_id=user_id,
        content="Test content",
    )

    mock_user_service.get_current_user.return_value = current_user
    mock_blog_repo.get_post_by_id.return_value = blog_post

    await blog_service.delete_post(post_id, user_token)

    mock_blog_repo.delete_post.assert_called_once_with(post_id)


@pytest.mark.asyncio
async def test_delete_post_not_found(
    blog_service: BlogService, mock_blog_repo: Mock, mock_user_service: Mock
) -> None:
    post_id = uuid.uuid4()
    user_token = "test_token"
    user_id = uuid.uuid4()
    current_user = Mock(id=user_id)

    mock_user_service.get_current_user.return_value = current_user
    mock_blog_repo.get_post_by_id.return_value = None

    with pytest.raises(BlogServiceException):
        await blog_service.delete_post(post_id, user_token)


@pytest.mark.asyncio
async def test_delete_post_unauthorized(
    blog_service: BlogService, mock_blog_repo: Mock, mock_user_service: Mock
) -> None:
    post_id = uuid.uuid4()
    user_token = "test_token"
    user_id = uuid.uuid4()
    different_user_id = uuid.uuid4()
    current_user = Mock(id=user_id)
    blog_post = BlogPost(
        id=post_id,
        user_id=different_user_id,
        content="Test content",
    )

    mock_user_service.get_current_user.return_value = current_user
    mock_blog_repo.get_post_by_id.return_value = blog_post

    with pytest.raises(BlogServiceUnAuthorizedException):
        await blog_service.delete_post(post_id, user_token)
