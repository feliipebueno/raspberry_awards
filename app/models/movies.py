"""Movies model implementation."""
from collections import defaultdict

from sqlalchemy import Column, Integer, String, Boolean, select
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

    def get_winning_movies(self) -> dict:
        """Get winning movies and calculate intervals for each producer.

        This method executes a query to select the producers and years of winning
        movies. It then calculates the intervals between the years each producer won.
        The results are sorted by the interval and returned, with the minimum and
        maximum intervals separately.

        Arguments:
            Has no arguments.

        Returns:
            dict: A dictionary with two keys:
                - "min" (list): A list containing the producer with the smallest
                    winning interval.
                - "max" (list): A list containing the producer with the largest
                    winning interval.

        """
        query = select(
            Movie.producers, Movie.year
        ).where(Movie.winner.is_(True)).order_by(Movie.producers, Movie.year)
        movies = (self.__session.execute(query)).all()

        producer_years = defaultdict(list)

        for movie in movies:
            cleaned_producers = movie.producers.replace(" and ", ",")
            producers = [producer.strip() for producer in cleaned_producers.split(",")]

            for producer in producers:
                producer_years[producer].append(movie.year)

        intervals = []
        for producer, years in producer_years.items():
            years.sort()
            for i in range(len(years) - 1):
                intervals.append({
                    "producer": producer,
                    "interval": years[i + 1] - years[i],
                    "previousWin": years[i],
                    "followingWin": years[i + 1]
                })

        sorted_intervals = sorted(intervals, key=lambda x: x["interval"])

        min_intervals = [sorted_intervals[0]]

        max_intervals = [sorted_intervals[-1]]

        return {"min": min_intervals, "max": max_intervals}
