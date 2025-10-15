from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship

from database import Base, CRUDMixin

if TYPE_CHECKING:
    from database.models import Match, User


class Move(Base, CRUDMixin):
    __tablename__ = "move"
    __repr_fields__ = (
        "match_id",
        "user_id",
        "coordinate_x",
        "coordinate_y",
        "move_order",
    )
    serialize_rules = ("-match", "-user")

    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey("match.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    coordinate_x = Column(Integer, nullable=False)
    coordinate_y = Column(Integer, nullable=False)
    move_order = Column(Integer, nullable=False)

    match: Mapped[Match] = relationship(
        "Match",
        foreign_keys=[match_id],
        back_populates="moves",
        passive_deletes=True,
    )

    user: Mapped[User] = relationship(
        "User",
        foreign_keys=[user_id],
        passive_deletes=True,
    )
