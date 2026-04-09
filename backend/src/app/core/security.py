# app/core/security.py

from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import jwt, JWTError

from app.core import Settings, get_settings


settings: Settings = get_settings()

ALGORITHM = 'HS256'


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    expire: datetime = datetime.now(timezone.utc) + (
        expires_delta or timedelta(
            minutes=settings.access_token_expire_minutes)
    )

    payload: dict[str, Any] = {
        'sub': subject,
        'exp': expire,
    }

    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    except JWTError as e:
        raise ValueError('Invalid token') from e
