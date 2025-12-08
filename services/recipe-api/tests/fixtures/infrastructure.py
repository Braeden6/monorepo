import pytest
from sqlmodel import Session, SQLModel, create_engine
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from recipe_api.shared.config import settings


@pytest.fixture(scope="session", name="postgres_container")
def postgres_container_fixture():
    with PostgresContainer("pgvector/pgvector:pg16", driver="psycopg2") as postgres:
        yield postgres

@pytest.fixture(scope="session", name="redis_container")
def redis_container_fixture():
    with RedisContainer("redis:7-alpine") as redis:
        yield redis

@pytest.fixture(scope="session", name="test_settings")
def test_settings_fixture(postgres_container, redis_container):
    original_db_url = settings.database_url
    original_redis_url = settings.redis_url

    settings.database_url = postgres_container.get_connection_url()
    redis_host = redis_container.get_container_host_ip()
    redis_port = redis_container.get_exposed_port(6379)
    settings.redis_url = f"redis://{redis_host}:{redis_port}/0"

    yield settings

    settings.database_url = original_db_url
    settings.redis_url = original_redis_url

@pytest.fixture(scope="session", name="engine")
def engine_fixture(test_settings):
    engine = create_engine(test_settings.database_url)

    from sqlalchemy import text
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

    SQLModel.metadata.create_all(engine)
    return engine

@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session
