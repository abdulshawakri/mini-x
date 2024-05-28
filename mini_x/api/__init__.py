from fastapi import APIRouter

from mini_x.api.v1.routes import auth, user, blog

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(blog.router, prefix="/blogs", tags=["blogs"])
