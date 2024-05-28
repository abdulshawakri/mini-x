import uuid
from unittest.mock import patch, Mock

import pytest
from passlib.context import CryptContext
from pydantic import SecretStr

from mini_x.api.v1.models.user import UserCreate, UserUpdate
from mini_x.infra.db.models.user import User
from mini_x.services.user.error import (
    UserServiceException,
    UserServiceUnAuthorizedException,
)
from mini_x.services.user.user_service import UserService
from mini_x.settings.secrets_settings import SecretSettings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture
def user_service(mock_user_repo: Mock, secret_settings: SecretSettings) -> UserService:
    return UserService(user_repository=mock_user_repo, secret_settings=secret_settings)


@pytest.fixture()
def user_create() -> UserCreate:
    return UserCreate(
        username="test_user",
        email="test@case.com",
        password=SecretStr("password123"),
        full_name="Test User",
        street_address="Test str. 123",
        zip_code="12345",
        city="Test City",
        country="Test Country",
    )


@pytest.fixture()
def hashed_password() -> str:
    return pwd_context.hash("password123")


@pytest.fixture()
def user(hashed_password: str) -> User:
    return User(
        id=uuid.uuid4(),
        username="test_user",
        email="test@case.com",
        hashed_password=hashed_password,
        full_name="Test User",
        street_address="Test str. 123",
        zip_code="12345",
        city="Test City",
        country="Test Country",
    )


@pytest.mark.asyncio
async def test_register_user(
    user_create: UserCreate, user_service: UserService, mock_user_repo: Mock
) -> None:
    mock_user_repo.get_by_email.return_value = None
    mock_user_repo.get_by_username.return_value = None

    with patch(
        "mini_x.authentication.auth_handler.get_password_hash",
        return_value=pwd_context.hash("password123"),
    ):
        user_read = await user_service.register_user(user_create)

    assert user_read.username == user_create.username
    assert user_read.email == user_create.email


@pytest.mark.asyncio
async def test_register_user_existing_email(
    user_create: UserCreate, user_service: UserService, mock_user_repo: Mock
) -> None:
    mock_user_repo.get_by_email.return_value = "existing_user"

    with pytest.raises(UserServiceException):
        await user_service.register_user(user_create)


@pytest.mark.asyncio
async def test_authenticate_user(
    user: User, user_service: UserService, mock_user_repo: Mock
) -> None:
    password = "password123"

    mock_user_repo.get_by_username.return_value = user

    with patch("mini_x.authentication.auth_handler.verify_password", return_value=True):
        authenticated_user = await user_service.authenticate_user(
            str(user.username), password
        )

    assert authenticated_user is not None
    assert authenticated_user.username == user.username


@pytest.mark.asyncio
async def test_authenticate_user_invalid_password(
    user: User, user_service: UserService, mock_user_repo: Mock
) -> None:
    password = "invalid_password"

    mock_user_repo.get_by_username.return_value = user

    with patch(
        "mini_x.authentication.auth_handler.verify_password", return_value=False
    ):
        authenticated_user = await user_service.authenticate_user(
            str(user.username), password
        )

    assert authenticated_user is None


@pytest.mark.asyncio
async def test_login_user(
    user: User, user_service: UserService, mock_user_repo: Mock
) -> None:
    password = "password123"

    mock_user_repo.get_by_username.return_value = user

    with patch("mini_x.authentication.auth_handler.verify_password", return_value=True):
        login_response = await user_service.login_user(str(user.username), password)

    assert login_response is not None
    assert "access_token" in login_response


@pytest.mark.asyncio
async def test_login_user_invalid_credentials(
    user: User, user_service: UserService, mock_user_repo: Mock
) -> None:
    password = "invalid_password"

    mock_user_repo.get_by_username.return_value = user

    with patch(
        "mini_x.authentication.auth_handler.verify_password", return_value=False
    ):
        login_response = await user_service.login_user(str(user.username), password)

    assert login_response is None


@pytest.mark.asyncio
async def test_update_user_profile(
    user: User, user_service: UserService, mock_user_repo: Mock
) -> None:
    user_from_token = "test_user"
    user_update = UserUpdate(
        full_name="Updated Test User",
        street_address="123 Updated St",
        zip_code="54321",
        city="Updated City",
        country="Updated Country",
    )

    updated_user = User(
        id=user.id,
        username=user.username,
        email=user.email,
        hashed_password=user.hashed_password,
        full_name=user_update.full_name,
        street_address=user_update.street_address,
        zip_code=user_update.zip_code,
        city=user_update.city,
        country=user_update.country,
        created_at=user.created_at,
    )

    mock_user_repo.get_by_username.return_value = user
    mock_user_repo.get_by_id.return_value = updated_user

    updated_user_read = await user_service.update_user_profile(
        user_from_token, user_update
    )

    assert updated_user_read.full_name == user_update.full_name
    assert updated_user_read.street_address == user_update.street_address
    assert updated_user_read.zip_code == user_update.zip_code
    assert updated_user_read.city == user_update.city
    assert updated_user_read.country == user_update.country


@pytest.mark.asyncio
async def test_get_current_user(
    user: User, user_service: UserService, mock_user_repo: Mock
) -> None:
    user_from_token = "test_user"

    mock_user_repo.get_by_username.return_value = user

    current_user_read = await user_service.get_current_user(user_from_token)

    assert current_user_read.username == user.username


@pytest.mark.asyncio
async def test_get_current_user_unauthorized(
    user_service: UserService, mock_user_repo: Mock
) -> None:
    user_from_token = "unauthorized_user"

    mock_user_repo.get_by_username.return_value = None

    with pytest.raises(UserServiceUnAuthorizedException):
        await user_service.get_current_user(user_from_token)
