"""
Create match table.

Revision ID: 4391f75b0508
Revises: a43e552d92e9
Create Date: 2025-10-13 11:59:34.633854

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "4391f75b0508"
down_revision: str | None = "a43e552d92e9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "match",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_x_id", sa.Integer(), nullable=False),
        sa.Column("user_o_id", sa.Integer(), nullable=False),
        sa.Column("winner_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_o_id"], ["user.id"], name=op.f("fk_match_user_o_id_user")
        ),
        sa.ForeignKeyConstraint(
            ["user_x_id"], ["user.id"], name=op.f("fk_match_user_x_id_user")
        ),
        sa.ForeignKeyConstraint(
            ["winner_id"], ["user.id"], name=op.f("fk_match_winner_id_user")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_match")),
    )


def downgrade() -> None:
    op.drop_table("match")
