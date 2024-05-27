from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from mini_x.api.v1.dependancies import get_user_service
from mini_x.api.v1.models.user import UserCreate, UserRead
from mini_x.constants import TOKEN_URL
from mini_x.services.user.user_service import UserService

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user: UserCreate, user_service: UserService = Depends(get_user_service)
) -> UserRead:
    try:
        registered_user = await user_service.register_user(user_create=user)
        return registered_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(get_user_service),
) -> dict[str, str]:
    token = await user_service.login_user(
        username=form_data.username, password=form_data.password
    )
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return token
