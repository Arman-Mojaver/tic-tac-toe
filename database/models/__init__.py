"""Import all models here so changes can be detected by alembic."""

from __future__ import annotations

from database.models.user import User

__all__: list[str] = ["User"]
