"""Import all models here so changes can be detected by alembic."""

from __future__ import annotations

from database.models.match import Match
from database.models.user import User

__all__: list[str] = ["Match", "User"]
