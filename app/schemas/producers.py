"""Implementation of Producers schemas."""

from pydantic import BaseModel


class ProducersSchema(BaseModel):
    """Producers Schemas."""

    producer: str
    interval: int
    previousWin: int
    followingWin: int


class ProducersResultSchema(BaseModel):
    """Producers Result Schema."""

    min: list[ProducersSchema]
    max: list[ProducersSchema]
