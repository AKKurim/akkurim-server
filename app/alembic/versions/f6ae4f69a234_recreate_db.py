"""recreate db

Revision ID: f6ae4f69a234
Revises:
Create Date: 2025-07-27 11:10:42.121248

"""

import re
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f6ae4f69a234"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with open("/app/app/resources/sql/updated_schema.sql", "r", encoding="utf-8") as f:
        sql = f.read()

    with open("/app/app/resources/sql/active_tenants.txt", "r", encoding="utf-8") as f:
        tenants = [each for each in f.read().split("\n") if each]

    conn = op.get_bind()

    for tenant_id in tenants:
        sql = re.sub("tenant_id", tenant_id, sql)
        conn.execute(sa.text(sql))


def downgrade() -> None:
    pass
