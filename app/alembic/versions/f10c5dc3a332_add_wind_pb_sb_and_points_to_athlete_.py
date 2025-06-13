"""add wind, pb_sb and points to athlete_meet_event

Revision ID: f10c5dc3a332
Revises: 6792015a95d7
Create Date: 2025-06-13 17:13:20.988177

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f10c5dc3a332"
down_revision: Union[str, None] = "6792015a95d7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # sql = 'alter table "tenant_id.athlete_meet_event" add column "wind" text, add column "pb_sb" text, add column "points" text;'
    # with open("/app/app/resources/sql/active_tenants.txt", "r", encoding="utf-8") as f:
    #     tenants = [each for each in f.read().split("\n") if each]

    # conn = op.get_bind()
    # for tenant_id in tenants:
    #     conn.execute(sa.text(sql.replace("tenant_id", tenant_id)))
    pass
    # manually in db since alembic thinks the table doesnt exist even tho it clearly does


def downgrade() -> None:
    pass
