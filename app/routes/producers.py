"""Producers routes implementation."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.sqlite import get_db
from app.models.movies import MovieDTO
from app.schemas.producers import ProducersResultSchema, ProducersSchema
from app.utils.exception import http_exception
from app.utils.logger import Logger

routes = APIRouter(prefix="/producers", tags=["Producers"])


@routes.get("/intervals", response_model=ProducersResultSchema)
def get_producer_intervals(
        session: Session = Depends(get_db)) -> ProducersResultSchema:
    """Get the minimum and maximum intervals between years for movie producers.

    This endpoint calculates the intervals between consecutive years of work for each
    producer in the dataset of winning movies. It returns producers who have the
    smallest and largest gaps between their consecutive wins.

    ### Arguments:
    - `session (Session)`: The database session used to access movie data.

    ### Returns:
    - `ProducersResultSchema:` A schema containing the minimum and maximum
        intervals for producers.
        - **min** (List[ProducersSchema]): A list of producers who have the
            smallest intervals.
        - **max** (List[ProducersSchema]): A list of producers who have the
            largest intervals.

    """
    try:
        movies = MovieDTO(session).get_winning_movies()
        intervals = {"min": [], "max": []}

        for movie in movies:
            entry = ProducersSchema(
                producer=movie.producers,
                interval=movie.interval,
                previousWin=movie.previousWin,
                followingWin=movie.followingWin
            )

            intervals[movie.type].append(entry)

        Logger(__name__).info("The movie breaks were requested.")
        return ProducersResultSchema(min=intervals["min"], max=intervals["max"])
    except Exception as err:
        msg = f"An error occurred while searching for intervals: {err}"
        Logger(__name__).error(msg)

        raise http_exception(
            message="An internal error has occurred. Please try again later.",
            status=500
        ) from err