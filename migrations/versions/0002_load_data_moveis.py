"""load data moveis

Revision ID: 0002
Revises: 0001
Create Date: 2025-03-03 10:15:37.610428

"""
from typing import Sequence, Union

import polars as pl
import sqlalchemy as sa
from alembic import op

from app.models.movies import Movie
from app.settings import env_data

# revision identifiers, used by Alembic.
revision: str = '0002'
down_revision: Union[str, None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    df = pl.read_csv(f"{env_data.ROOT_DIR}/data/Movielist.csv", separator=";")
    bind = op.get_bind()


    df = df.with_columns(
        pl.when(df["winner"].is_null())
        .then(False)
        .otherwise(df["winner"].str.to_lowercase() == "yes")
        .alias("winner")
    )

    for row in df.iter_rows(named=True):
        bind.execute(
            Movie.__table__.insert().values(
                year=row["year"],
                title=row["title"],
                studios=row["studios"],
                producers=row["producers"],
                winner=row["winner"]
            )
        )
    # ### end Alembic commands ###

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()

    bind.execute(sa.delete(Movie))

    bind.execute(sa.sql.text('DELETE FROM sqlite_sequence WHERE name="movies"'))

    bind.execute(sa.sql.text('VACUUM'))
    # ### end Alembic commands ###
