# app/schemas/categories.py

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.domain import CategoryType


class CategoryGetSchema(BaseModel):
    id: UUID


class CategoryUpdateSchema(BaseModel):
    id: UUID
    category_name: Optional[str] = None
    type: Optional[CategoryType] = None
    parent_name: Optional[str] = None


class CategoryCreateSchema(BaseModel):
    category_name: str
    type: CategoryType
    parent_name: Optional[str] = None


class CategoryResponseSchema(BaseModel):
    id: UUID
    category_name: str
    type: CategoryType
    parent_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
