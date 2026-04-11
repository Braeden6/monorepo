from collections.abc import Generator

from sqlmodel import Session, create_engine

from recipe_api.shared.config import settings

_engine = None
_last_url = None


def get_engine():
    global _engine, _last_url
    if _engine is None or _last_url != settings.database_url:
        _engine = create_engine(
            settings.database_url,
            echo=settings.log_level == "debug",
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
        _last_url = settings.database_url
    return _engine


def get_session() -> Generator[Session, None, None]:
    with Session(get_engine()) as session:
        yield session


def get_db_session() -> Session:
    return Session(get_engine())
