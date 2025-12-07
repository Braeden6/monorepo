from collections.abc import Generator

from sqlmodel import Session, create_engine

from recipe_api.shared.config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.log_level == "debug",
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def get_db_session() -> Session:
    return Session(engine)
