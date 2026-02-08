"""merge_training_time_into_group

Revision ID: 39e2194b2589
Revises: e0b6edaa9e6e
Create Date: 2026-02-08 10:37:20.259440

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "39e2194b2589"
down_revision: Union[str, None] = "e0b6edaa9e6e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("group", sa.Column("day_of_week", sa.String(), nullable=True))
    op.add_column("group", sa.Column("summer_time", sa.Time(), nullable=True))
    op.add_column("group", sa.Column("winter_time", sa.Time(), nullable=True))
    op.add_column("group", sa.Column("duration_summer", sa.Integer(), nullable=True))
    op.add_column("group", sa.Column("duration_winter", sa.Integer(), nullable=True))
    op.add_column(
        "group", sa.Column("default_location_summer", sa.String(), nullable=True)
    )
    op.add_column(
        "group", sa.Column("default_location_winter", sa.String(), nullable=True)
    )

    op.execute(
        """
        UPDATE "group"
        SET 
            day_of_week = tt.day,
            summer_time = tt.summer_time,
            winter_time = tt.winter_time,
            duration_summer = tt.duration_summer,
            duration_winter = tt.duration_winter
            updated_at = now()
        FROM training_time tt
        WHERE "group".training_time_id = tt.id
    """
    )

    op.alter_column("group", "day_of_week", nullable=False)
    op.alter_column("group", "summer_time", nullable=False)
    op.alter_column("group", "winter_time", nullable=False)
    op.alter_column("group", "duration_summer", nullable=False)
    op.alter_column("group", "duration_winter", nullable=False)

    op.drop_constraint("group_training_time_id_fkey", "group", type_="foreignkey")
    op.drop_column("group", "training_time_id")
    op.drop_table("training_time")


def downgrade() -> None:
    pass
