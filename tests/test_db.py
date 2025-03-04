"""Implementation of the database session unit test."""

from sqlalchemy.orm import Session

from app.db.sqlite import get_db


def test_get_db(session: Session) -> None:
    """Test the database session retrieval.

    This test verifies that the `get_db` function returns a new instance of a
    `Session`, different from the one provided as a fixture, ensuring that a new
    session is created for each request.

    Arguments:
        session: The session used in the test, provided by the `session` fixture.

    Asserts:
        - The retrieved instance is of type `Session`.
        - The retrieved instance is not the same as the original session.
        - The retrieved instance is different from the original session, ensuring
          a new session is created.

    """
    db_instance = next(get_db())

    assert isinstance(db_instance, Session)

    assert db_instance is not session
    assert db_instance != session
