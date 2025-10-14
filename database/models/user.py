from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from database import Base, CRUDMixin

if TYPE_CHECKING:
    from database.models import Match


class User(Base, CRUDMixin):
    __tablename__ = "user"
    __repr_fields__ = ("name",)
    serialize_rules = ("-password", "-matches_as_x", "-matches_as_o")

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)

    matches_as_x: Mapped[list[Match]] = relationship(
        "Match",
        foreign_keys="Match.user_x_id",
        back_populates="user_x",
        passive_deletes=True,
    )

    matches_as_o: Mapped[list[Match]] = relationship(
        "Match",
        foreign_keys="Match.user_o_id",
        back_populates="user_o",
        passive_deletes=True,
    )
