"""Movies model implementation."""

from collections.abc import Sequence

from sqlalchemy import Column, Integer, String, Boolean, text
from sqlalchemy.orm import Session

from app.db.sqlite import Base


class Movie(Base):
    """Represents a movie entity in the database.

    This SQLAlchemy model defines the structure of the `movies` table, storing
    information about movies, including their title, release year, studios,
    producers, and whether they won an award.

    Table Name:
        movies

    Attributes:
        id (int): The unique identifier for the movie (Primary Key).
        year (int): The release year of the movie.
        title (str): The title of the movie.
        studios (str): The studio(s) responsible for the movie.
        producers (str): The producer(s) associated with the movie.
        winner (bool): Indicates whether the movie won an award (default is False).

    """

    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    studios = Column(String(255), nullable=False, index=True)
    producers = Column(String(255), nullable=False, index=True)
    winner = Column(Boolean, default=False, nullable=False)


class MovieDTO:
    """Data Transfer Object for movies.

    This class serves as a Data Transfer Object (DTO) for movie-related data. It
    interacts with the database session to retrieve movie data, specifically focused
    on movies that have won awards. It provides methods to query winning movies and
    return relevant information.

    Attributes:
        __session (Session): The SQLAlchemy session used to interact with the database.

    Methods:
        get_winning_movies(): Retrieves all winning movies and their associated
            producers.

    """

    def __init__(self, session: Session):
        """Initialize the MovieDTO with a database session.

        This method initializes the MovieDTO instance with a SQLAlchemy session,
        which will be used to query movie data from the database.

        Arguments:
            session (Session): The database session used to interact with the movie
                database.

        Returns:
            None: Method without data return.

        """
        self.__session = session

    def get_winning_movies(self) -> Sequence:
        """Get all winning movies and their associated producers.

        This method queries the `Movie` table for all movies that have won awards.
        It retrieves the year and producers of the winning movies.

        Arguments:
            Has no arguments.

        Returns:
            Sequence: A sequence (e.g., list) of tuples, where each tuple contains the
                year and the producers of a winning movie.

        """
        sql = """
           WITH RankedMovies AS (
            SELECT 
                producers, 
                year, 
                LAG(year) OVER (PARTITION BY producers ORDER BY year) AS previousWin
            FROM movies 
            WHERE winner = 1
            ),
            Intervals AS (
                SELECT 
                    producers,
                    year AS followingWin,
                    previousWin,
                    (year - previousWin) AS interval
                FROM RankedMovies
                WHERE previousWin IS NOT NULL
            ),
            MinInterval AS (
                SELECT * 
                FROM Intervals 
                WHERE interval = (SELECT MIN(interval) FROM Intervals)
            ),
            MaxInterval AS (
                SELECT * 
                FROM Intervals
                WHERE interval = (SELECT MAX(interval) FROM Intervals)
            )
            SELECT 'min' AS type, producers, interval, previousWin, followingWin 
                FROM MinInterval
                
            UNION ALL
            SELECT 'max' AS type, producers, interval, previousWin, followingWin 
            FROM MaxInterval;
        """
        query = text(sql)
        return self.__session.execute(query).all()
