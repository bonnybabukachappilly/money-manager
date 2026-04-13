# app/db/models/categories.py

from typing import Any, TYPE_CHECKING, Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlalchemy import (
    String, ForeignKey, DateTime,
    Enum as SQLEnum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db import Base
from app.domain import CategoryType

if TYPE_CHECKING:
    from .user import UserModel


class CategoryModel(Base):
    __tablename__: Any = 'categories'

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    user: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    category_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )

    type: Mapped[CategoryType] = mapped_column(
        SQLEnum(CategoryType),
        nullable=False,
        default=CategoryType.EXPENSE
    )

    parent_id: Mapped[Optional[UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey('categories.id', ondelete='SET NULL'),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    parent_relationship: Mapped[Optional["CategoryModel"]] = relationship(
        "CategoryModel",
        remote_side=[id],
        lazy="select"
    )

    user_relationship: Mapped['UserModel'] = relationship(
        'UserModel',
        lazy='raise'
    )
