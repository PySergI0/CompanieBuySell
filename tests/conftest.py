import asyncio
import asyncpg
from pydantic_settings import BaseSettings, SettingsConfigDict
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator

from main import app
from app.database import Base, get_db
from app.config import setup_log


log = setup_log(__name__)


class TestDBConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".test.env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="TEST_DB_",
    )
    user: str
    password: str
    host: str
    name: str
    port: str

    @property
    def get_test_db_base_url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/"

    @property
    def get_test_db_name(self):
        return f"{self.name}"


test_db_config = TestDBConfig()

TEST_DB_NAME = test_db_config.get_test_db_name
TEST_DB_BASE_URL = test_db_config.get_test_db_base_url
TEST_DB_URL = f"{TEST_DB_BASE_URL}{TEST_DB_NAME}"


@pytest_asyncio.fixture(scope="session")
async def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database(event_loop):
    log.debug(f"Start prepare_database")
    """Prepare test database and clean up afterwards."""
    # Create test database
    conn = await asyncpg.connect(
        f"postgres://{test_db_config.user}:{test_db_config.password}@{test_db_config.host}:{test_db_config.port}/postgres"
    )
    try:
        await conn.execute(f"CREATE DATABASE {TEST_DB_NAME}")
    except asyncpg.DuplicateDatabaseError:
        pass
    finally:
        log.debug(f"Close conn")
        await conn.close()

    yield

    conn = await asyncpg.connect(
        f"postgres://{test_db_config.user}:{test_db_config.password}@{test_db_config.host}:{test_db_config.port}/postgres"
    )
    try:
        await conn.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{TEST_DB_NAME}'
        """)
        await conn.execute(f"DROP DATABASE {TEST_DB_NAME}")
    finally:
        await conn.close()


@pytest_asyncio.fixture(scope="function")
async def engine():
    log.debug(f"Start engine")
    engine = create_async_engine(
        TEST_DB_URL,
        pool_pre_ping=True,
        echo=False,
        pool_size=10,
        max_overflow=20
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture()
async def db_session(engine):
    log.debug(f"Start db_session")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False
    )

    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest_asyncio.fixture
async def override_get_db(db_session):
    log.debug(f"Start override_get_db")

    async def _override_get_db():
        try:
            yield db_session
        finally:
            await db_session.close()

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def async_client(override_get_db) -> AsyncGenerator[AsyncClient, None]:
    """Create an async client for testing."""
    log.debug(f"Start async_client")
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
