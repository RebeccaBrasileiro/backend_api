# tests/conftest.py

import os
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from turismo.infra.database import Base
from turismo.api.main import app
from turismo.api import deps
from asgi_lifespan import LifespanManager


# ⚡️ 1) Força o DATABASE_URL a ser o de teste
os.environ["DATABASE_URL"] = os.getenv(
    "DATABASE_URL_TEST",
    "postgresql+asyncpg://test_user:test_password@db_test:5432/turismo_test",
)

# Guarda para uso abaixo
TEST_DATABASE_URL = os.environ["DATABASE_URL"]


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Evita conflito de loops no pytest-asyncio."""
    import asyncio

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def setup_engine():
    """Cria engine e sessão de teste."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    # Cria todas as tabelas para o teste
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine, async_session

    # Teardown se quiser dropar tudo de novo no final
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(setup_engine):
    """Cria uma sessão de banco por teste."""
    _, async_session = setup_engine
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session):
    """Cria cliente de teste com override de dependências."""

    async def override_get_db_session():
        yield db_session

    app.dependency_overrides[deps.get_db_session] = override_get_db_session

    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

    app.dependency_overrides.clear()
