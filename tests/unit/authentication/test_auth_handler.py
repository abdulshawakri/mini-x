import pytest
from passlib.context import CryptContext

from mini_x.authentication.auth_handler import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token,
    SecretSettings,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.mark.parametrize(
    "plain_password, hashed_password, expected",
    [
        ("password123", pwd_context.hash("password123"), True),
        ("password123", pwd_context.hash("differentpassword"), False),
    ],
    ids=["correct_password_case", "incorrect_password_case"],
)
def test_verify_password(
    plain_password: str, hashed_password: str, expected: bool
) -> None:
    assert verify_password(plain_password, hashed_password) == expected


@pytest.mark.parametrize(
    "password",
    [
        "password123",
        "anotherpassword",
    ],
    ids=["hash_password123_case", "hash_anotherpassword_case"],
)
def test_get_password_hash(password: str) -> None:
    hashed_password = get_password_hash(password)
    assert pwd_context.verify(password, hashed_password)


def test_create_access_token(
    secret_settings: SecretSettings, sample_data: dict[str, str]
) -> None:
    token = create_access_token(data=sample_data, secret_settings=secret_settings)
    assert isinstance(token, str)


def test_decode_access_token(
    secret_settings: SecretSettings, sample_data: dict[str, str]
) -> None:
    token = create_access_token(data=sample_data, secret_settings=secret_settings)
    decoded_data = decode_access_token(token, secret_settings)
    assert decoded_data is not None
    assert decoded_data["sub"] == sample_data["sub"]


def test_expired_access_token(
    secret_settings: SecretSettings, sample_data: dict[str, str]
) -> None:
    expired_settings = SecretSettings(
        key="test_secret", algorithm="HS256", access_token_expire_minutes=-1
    )
    token = create_access_token(data=sample_data, secret_settings=expired_settings)
    decoded_data = decode_access_token(token, secret_settings)
    assert decoded_data is None


def test_decode_access_token_invalid_signature(secret_settings: SecretSettings) -> None:
    invalid_token = "invalid.token.signature"
    decoded_data = decode_access_token(invalid_token, secret_settings)
    assert decoded_data is None


def test_decode_access_token_with_invalid_algorithm(
    secret_settings: SecretSettings, sample_data: dict[str, str]
) -> None:
    token = create_access_token(data=sample_data, secret_settings=secret_settings)
    invalid_algorithm_settings = SecretSettings(
        key=secret_settings.key, algorithm="blabla", access_token_expire_minutes=30
    )
    decoded_data = decode_access_token(token, invalid_algorithm_settings)
    assert decoded_data is None
