from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.database import init_db, close_db
from app.graphql.schema import schema
from app.graphql.context import make_edition_graphql_app


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="D&D Character Sheet API",
    version="0.1.0",
    description="API de referência para fichas de personagem D&D (edições 2014 e 2024)",
    lifespan=lifespan,
)

app.mount("/api/5e", make_edition_graphql_app(schema, edition="5e"))
app.mount("/api/5_5e", make_edition_graphql_app(schema, edition="5.5e"))


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
