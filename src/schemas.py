from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, PositiveInt


class CreateMatchData(BaseModel):
    user_x_id: PositiveInt
    user_o_id: PositiveInt


class MoveData(BaseModel):
    match_id: PositiveInt
    user_id: PositiveInt
    coordinate_x: Literal[0, 1, 2]
    coordinate_y: Literal[0, 1, 2]

    def coordinates(self) -> tuple[int, int]:
        return self.coordinate_x, self.coordinate_y


class GameStatus(BaseModel):
    match_id: int
    user_x_id: int
    user_o_id: int
    user_turn: int | None = None
    user_x_coordinates: list[list[int]] = Field(default_factory=list)
    user_o_coordinates: list[list[int]] = Field(default_factory=list)
    winner_id: int | None = None
