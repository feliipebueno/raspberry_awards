"""Database access implementation."""

from collections.abc import Generator

from prettyconf import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL=config("DATABASE_URL", default=None)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Provide a database session.

    This function creates a new database session using `SessionLocal`, yields it for
    use, and ensures that the session is properly closed after execution.

    Arguments:
        Has no arguments.

    Returns:
        yields: session a SQLAlchemy database session.

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()