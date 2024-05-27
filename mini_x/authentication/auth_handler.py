from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

from mini_x.settings.secrets_settings import SecretSettings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    secret_settings: SecretSettings,
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=secret_settings.access_token_expire_minutes
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, secret_settings.key, algorithm=secret_settings.algorithm
    )
    return encoded_jwt


def decode_access_token(
    token: str, secret_settings: SecretSettings
) -> dict[str, str] | None:
    try:
        payload = jwt.decode(
            token, secret_settings.key, algorithms=[secret_settings.algorithm]
        )
        return payload
    # TODO: Raise HTTP Exception instead
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None
