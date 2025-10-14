from __future__ import annotations

from pydantic import BaseModel, Field, PositiveInt


class MatchUsers(BaseModel):
    user_x_id: PositiveInt
    user_o_id: PositiveInt


class GameStatus(BaseModel):
    match_id: int
    user_x_id: int
    user_o_id: int
    user_turn: int | None = None
    user_x_coordinates: list[list[int]] = Field(default_factory=list)
    user_o_coordinates: list[list[int]] = Field(default_factory=list)
    winner_id: int | None = None
