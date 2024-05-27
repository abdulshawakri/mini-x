from typing import Annotated

from fastapi import APIRouter, Depends

from mini_x.api.v1.dependancies import get_current_user
from mini_x.api.v1.models.user import UserRead

router = APIRouter()


@router.get("/me")
async def read_users_me(
    current_user: Annotated[UserRead, Depends(get_current_user)],
) -> UserRead:
    return current_user
