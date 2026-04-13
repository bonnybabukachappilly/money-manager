# app/main.py

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
from asyncio import sleep

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.logging import configure_logging
from app.db import engine
from fastapi.responses import JSONResponse

from app.api.v1 import v1_router

configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    connected = False
    retries = 5
    while not connected and retries > 0:
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
                connected = True
                break
        except Exception:
            retries -= 1
            await sleep(2)
    else:
        raise RuntimeError("Database connection failed during startup")

    yield
    await engine.dispose()


app = FastAPI(
    title="Finance Dashboard API",
    version="1.0.0",
    lifespan=lifespan,
)

# ── Middleware ────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routes ────────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check() -> JSONResponse:
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"

    payload: dict[str, str] = {
        "status": "ok" if db_status == "ok" else "degraded",
        "db": db_status,
        "version": "1.0.0"
    }

    return JSONResponse(content=payload,
                        status_code=200 if db_status == "ok" else 503)


app.include_router(v1_router)
