from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class BlogPostBase(BaseModel):
    content: str = Field(..., max_length=500)


class BlogPostCreate(BlogPostBase):
    pass


class BlogPostUpdate(BlogPostBase):
    pass


class BlogPostRead(BlogPostBase):
    id: UUID
    user_id: UUID

    model_config = ConfigDict(from_attributes=True)


class BlogPostDelete(BaseModel):
    post_id: UUID
    message: str
