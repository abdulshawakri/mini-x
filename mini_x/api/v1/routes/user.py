from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from mini_x.api.v1.dependancies import get_current_user_from_token, get_user_service
from mini_x.api.v1.models.user import UserRead, UserUpdate
from mini_x.services.user.error import UserServiceUnAuthorizedException
from mini_x.services.user.user_service import UserService

router = APIRouter()


@router.get("/me")
async def read_users_me(
    user_from_token: Annotated[str, Depends(get_current_user_from_token)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    try:
        current_user = await user_service.get_current_user(user_from_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    return current_user


@router.put("/me")
async def update_user_me(
    user_update: UserUpdate,
    user_from_token: Annotated[str, Depends(get_current_user_from_token)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    try:
        updated_user = await user_service.update_user_profile(
            user_from_token, user_update
        )
        return updated_user
    except UserServiceUnAuthorizedException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    except Exception as e:
        import logging

        logging.info(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
