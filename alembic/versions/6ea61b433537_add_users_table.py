"""add users table

Revision ID: 6ea61b433537
Revises: ad7e9f787097
Create Date: 2024-06-22 16:29:34.107513

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision: str = "6ea61b433537"
down_revision: Union[str, None] = "ad7e9f787097"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("passowrd", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("users")
