from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship

from database import Base, CRUDMixin

if TYPE_CHECKING:
    from database.models import User
    from database.models.move import Move


class Match(Base, CRUDMixin):
    __tablename__ = "match"
    __repr_fields__ = ("user_x_id", "user_o_id", "winner_id")
    serialize_rules = ("-user_x", "-user_o", "-winner")

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_x_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user_o_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    winner_id = Column(
        Integer,
        ForeignKey("user.id"),
        nullable=True,
        default=None,
    )

    user_x: Mapped[User] = relationship(
        "User",
        foreign_keys=[user_x_id],
        back_populates="matches_as_x",
        passive_deletes=True,
    )

    user_o: Mapped[User] = relationship(
        "User",
        foreign_keys=[user_o_id],
        back_populates="matches_as_o",
        passive_deletes=True,
    )

    winner: Mapped[User | None] = relationship(
        "User",
        foreign_keys=[winner_id],
        passive_deletes=True,
    )

    moves: Mapped[list[Move]] = relationship(
        "Move",
        foreign_keys="Move.match_id",
        back_populates="match",
        passive_deletes=True,
    )

    def user_ids(self) -> tuple[int, int]:
        return self.user_x_id, self.user_o_id
