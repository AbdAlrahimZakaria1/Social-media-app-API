"""add foreign key owner_id to posts

Revision ID: ed86dfa6803d
Revises: 6ea61b433537
Create Date: 2024-06-22 16:43:17.612186

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ed86dfa6803d"
down_revision: Union[str, None] = "6ea61b433537"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", "posts")
    op.drop_column("posts", "owner_id")
