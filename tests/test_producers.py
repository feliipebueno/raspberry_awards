"""Implementation of the unit test for the producers route."""

from unittest import mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.movies import Movie, MovieDTO


@pytest.fixture
def mock_data(session: Session) -> Session:
    """Create winner movie data in an in-memory database with the correct fields.

    This fixture sets up five movie records in the database with predefined values.
    Each movie is marked as a winner and contains details like year, title, studio,
    and producer. These records are added to the session and committed to the database
    for use in tests.

    Arguments:
        session: The database session used to interact with the database.

    Returns:
        Session: The database session with the added movie records.

    """
    movie_1 = Movie(year=1990, title="Movie 1", studios="Studio 1",
                    producers="Producer X", winner=True)
    movie_2 = Movie(year=2002, title="Movie 2", studios="Studio 1",
                    producers="Producer X", winner=True)
    movie_3 = Movie(year=2010, title="Movie 3", studios="Studio 2",
                    producers="Producer Y", winner=True)
    movie_4 = Movie(year=2010, title="Movie 3", studios="Studio 2",
                    producers="Producer Y", winner=True)
    movie_5 = Movie(year=2020, title="Movie 4", studios="Studio 2",
                    producers="Producer Y", winner=True)

    session.add_all([movie_1, movie_2, movie_3, movie_4, movie_5])
    session.commit()
    return session

def test_get_producer_intervals_exception(app_client: TestClient) -> None:
    """Test handling of an exception when fetching producer intervals.

    This test simulates an error in the `get_winning_movies` method of the `MovieDTO`
    class by mocking it to raise an exception. It verifies that the API returns a 500
    status code and a generic error message.

    Arguments:
        app_client: The test client to interact with the FastAPI application.

    Asserts:
        - The response status code is 500, indicating an internal server error.
        - The response contains the expected error message in JSON format.

    """
    with mock.patch.object(MovieDTO, 'get_winning_movies',
                           side_effect=Exception("Forced error")):

        response = app_client.get("api/producers/intervals")

        assert response.status_code == 500
        assert response.json() == {
            "detail": "An internal error has occurred. Please try again later."}

def test_get_producer_intervals(override_get_db: Session,
                                mock_data: Session, app_client: TestClient) -> None:
    """Test the successful retrieval of producer intervals.

    This test checks that the `GET /api/producers/intervals` endpoint correctly
    returns the minimum and maximum intervals between consecutive movie wins for
    producers. It verifies that the response status code is 200, and that the response
    contains the expected data structure.

    Arguments:
        override_get_db: The session used to override the database dependency.
        mock_data: The session used to populate the database with mock data for
            testing.
        app_client: The test client to interact with the FastAPI application.

    Asserts:
        - The response status code is 200, indicating successful retrieval.
        - The response contains the "min" and "max" keys.
        - The "min" and "max" keys have non-zero lengths, indicating valid data.

    """
    response = app_client.get("api/producers/intervals")

    assert response.status_code == 200

    data = response.json()

    assert "min" in data
    assert "max" in data

    assert len(data["min"]) > 0
    assert len(data["max"]) > 0
