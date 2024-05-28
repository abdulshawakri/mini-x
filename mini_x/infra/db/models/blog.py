import uuid
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from mini_x.infra.db.base import Base


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(String(500), nullable=False)
    created_at = Column(
        DateTime(timezone=False), default=datetime.utcnow, nullable=False
    )
    # YES we provide free edit without subscription!
    updated_at = Column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    author = relationship("User", back_populates="posts")
