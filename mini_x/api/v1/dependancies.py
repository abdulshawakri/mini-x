from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from mini_x.authentication.auth_handler import decode_access_token
from mini_x.constants import TOKEN_URL
from mini_x.infra.db.session import get_session
from mini_x.repositories.blog.blog import BlogRepository
from mini_x.repositories.blog.blog_abc import BlogRepositoryABC
from mini_x.repositories.user.user import UserRepository
from mini_x.repositories.user.user_abc import UserRepositoryABC
from mini_x.services.blog.blog_service import BlogService
from mini_x.services.user.user_service import UserService
from mini_x.settings.secrets_settings import get_secret_settings, SecretSettings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRepositoryABC:
    return UserRepository(session)


def get_user_service(
    user_repo: Annotated[UserRepositoryABC, Depends(get_user_repository)],
    secret_settings: Annotated[SecretSettings, Depends(get_secret_settings)],
) -> UserService:
    return UserService(user_repo, secret_settings)


def get_blog_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> BlogRepositoryABC:
    return BlogRepository(session)


def get_blog_service(
    blog_repo: Annotated[BlogRepositoryABC, Depends(get_blog_repository)],
) -> BlogService:
    return BlogService(blog_repo)


async def get_current_user_from_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    secret_settings: Annotated[SecretSettings, Depends(get_secret_settings)],
) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token, secret_settings)
    if payload is None:
        raise credentials_exception

    username: str | None = payload.get("sub")
    if username is None:
        raise credentials_exception
    return username
