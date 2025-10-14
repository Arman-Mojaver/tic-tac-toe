from __future__ import annotations

from sqlalchemy import Column, Integer, String

from database import Base, CRUDMixin


class User(Base, CRUDMixin):
    __tablename__ = "user"
    __repr_fields__ = ("name",)
    serialize_rules = ("-password",)

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
