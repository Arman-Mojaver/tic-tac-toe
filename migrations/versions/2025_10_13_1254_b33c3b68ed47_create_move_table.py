"""
Create move table.

Revision ID: b33c3b68ed47
Revises: 4391f75b0508
Create Date: 2025-10-13 12:54:08.125739

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "b33c3b68ed47"
down_revision: str | None = "4391f75b0508"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "move",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("match_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("coordinate_x", sa.Integer(), nullable=False),
        sa.Column("coordinate_y", sa.Integer(), nullable=False),
        sa.Column("move_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["match_id"], ["match.id"], name=op.f("fk_move_match_id_match")
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], name=op.f("fk_move_user_id_user")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_move")),
    )


def downgrade() -> None:
    op.drop_table("move")
