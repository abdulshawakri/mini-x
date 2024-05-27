import uuid
from datetime import timedelta

from mini_x.api.v1.models.user import UserCreate, UserRead
from mini_x.authentication.auth_handler import (
    get_password_hash,
    verify_password,
    create_access_token,
)
from mini_x.infra.db.models.user import User
from mini_x.repositories.user.user_abc import UserRepositoryABC
from mini_x.settings.secrets_settings import SecretSettings


class UserService:
    def __init__(
        self, user_repository: UserRepositoryABC, secret_settings: SecretSettings
    ) -> None:
        self._user_repository = user_repository
        self._secret_settings = secret_settings

    async def register_user(self, user_create: UserCreate) -> UserRead:
        existing_user = await self._user_repository.get_by_email(user_create.email)
        # TODO: Create custom exception
        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = get_password_hash(user_create.password.get_secret_value())
        new_user = User(
            id=uuid.uuid4(),
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
            full_name=user_create.full_name,
            street_address=user_create.street_address,
            zip_code=user_create.zip_code,
            city=user_create.city,
            country=user_create.country,
        )
        await self._user_repository.upsert(new_user)

        return UserRead.from_orm(new_user)

    async def authenticate_user(self, username: str, password: str) -> User | None:
        user = await self._user_repository.get_by_username(username)
        if not user or not verify_password(password, str(user.hashed_password)):
            return None
        return user

    async def get_username(self, username: str) -> User | None:
        return await self._user_repository.get_by_username(username)

    async def login_user(self, username: str, password: str) -> dict[str, str] | None:
        user = await self.authenticate_user(username, password)

        if not user:
            return None

        access_token_expires = timedelta(
            minutes=self._secret_settings.access_token_expire_minutes
        )
        access_token = create_access_token(
            data={"sub": user.username},
            secret_settings=self._secret_settings,
            expires_delta=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}
