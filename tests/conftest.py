"""Implementation of test management."""

import os
from collections.abc import Iterator
from typing import Callable

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from app.db.sqlite import Base, get_db
from app.settings import env_data
from main import app


@pytest.fixture(scope="module")
def engine()-> Iterator[Engine]:
    """Create and manage an SQLite database engine for testing.

    This fixture creates a new SQLite engine for testing purposes, specifically
    using an in-memory SQLite database file (`awards-test.sqlite3`). It also
    ensures that the database schema is created before the test starts and dropped
    after the test concludes. The database file is removed after each test to
    maintain isolation.

    Arguments:
        Has no arguments.

    Returns:
        Iterator[Engine]: An SQLAlchemy `Engine` object used to connect to the
            database for the test.

    """
    engine = create_engine(
        "sqlite:///data/awards-test.sqlite3", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

    file_database = f"{env_data.ROOT_DIR}/data/awards-test.sqlite3"
    if os.path.exists(file_database):
        os.remove(file_database)

@pytest.fixture(scope="function")
def session(engine: create_engine) -> Session:
    """Create a new database session for each test.

    This fixture creates a new SQLAlchemy session using the provided engine for each
    test. The session is automatically rolled back after the test, ensuring that
    changes made during testing do not persist.

    Arguments:
        engine (create_engine): The SQLAlchemy engine to be used for the session.

    Returns:
        Session: A new SQLAlchemy session for interacting with the database.

    """
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session_local()
    yield db
    db.close()

@pytest.fixture
def override_get_db(session: Session) -> Callable:
    """Override the get_db dependency for testing with a session.

    This fixture provides an overridden version of the `get_db` dependency that yields
    a database session for testing purposes. It ensures that the session is properly
    closed after use.

    Arguments:
        session (Session): The session instance to be used in place of the default
          database session.

    Returns:
        Callable: A function that yields the `session` for use in the test, and
            ensures it is closed after use.

    """
    def _override_get_db():
        """."""
        try:
            yield session
        finally:
            session.close()

    return _override_get_db


@pytest.fixture(scope="function")
def get_app(override_get_db: Callable) -> FastAPI:
    """Provide the FastAPI app instance with overridden dependencies for testing.

    This fixture overrides the `get_db` dependency with the provided `override_get_db`
    function, allowing for controlled database interactions during tests.

    Arguments:
        override_get_db (Callable): A function to override the default `get_db`
            dependency.

    Returns:
        FastAPI: The FastAPI app instance with the overridden dependencies.

    """
    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture(scope="function")
def app_client(get_app: FastAPI) -> TestClient:
    """Provide a test client for making requests to the FastAPI app.

    This fixture creates a TestClient instance using the FastAPI application passed
    through the `get_app` fixture. The test client can be used in test functions
    to simulate HTTP requests and interact with the application.

    The scope of the fixture is set to "function", meaning a new instance of the
    TestClient will be provided for each test function that depends on this fixture.

    Arguments:
        get_app (FastAPI): The FastAPI application instance to be used for testing.

    Returns:
        TestClient: A TestClient instance that allows making HTTP requests to the app.

    """
    with TestClient(app=get_app, base_url="http://test") as client:
        yield client
