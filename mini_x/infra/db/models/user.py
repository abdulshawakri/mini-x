import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from mini_x.infra.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
    full_name = Column(String)
    street_address = Column(String, nullable=True)
    zip_code = Column(String, nullable=True, index=True)
    city = Column(String, nullable=True, index=True)
    country = Column(String, nullable=True, index=True)

    created_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )