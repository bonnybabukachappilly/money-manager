# app/domain/entities/categories.py

from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum


class CategoryType(str, Enum):
    INCOME = 'income'
    EXPENSE = 'expense'


@dataclass
class Category:
    id: UUID
    user: UUID
    category_name: str
    type: CategoryType
    created_at: datetime
    parent_id: Optional[UUID] = None
    parent_name: Optional[str] = None
