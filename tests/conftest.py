from unittest.mock import Mock

import pytest

from mini_x.repositories.blog.blog import BlogRepository
from mini_x.repositories.user.user import UserRepository
from mini_x.settings.secrets_settings import SecretSettings


@pytest.fixture
def secret_settings():
    return SecretSettings(
        key="test_secret", algorithm="HS256", access_token_expire_minutes=30
    )


@pytest.fixture
def sample_data():
    return {"sub": "test_user"}


@pytest.fixture
def mock_user_repo() -> Mock:
    return Mock(spec=UserRepository)


@pytest.fixture
def mock_blog_repo() -> Mock:
    return Mock(spec=BlogRepository)
