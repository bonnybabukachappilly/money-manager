# app/db/models/user.py

from typing import Any
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import UUID, uuid4

from app.db import Base


class UserModel(Base):
    __tablename__: Any = 'users'

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    first_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
