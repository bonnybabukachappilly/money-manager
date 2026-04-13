# app/domain/entities/user.py

from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:

    id: UUID
    first_name: str
    last_name: str
    email: str
    hashed_password: str
    is_active: bool = True
