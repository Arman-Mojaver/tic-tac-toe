from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, PositiveInt


# Request schemas
class CreateMatchData(BaseModel):
    user_x_id: PositiveInt
    user_o_id: PositiveInt


class CreateMoveData(BaseModel):
    match_id: PositiveInt
    user_id: PositiveInt
    coordinate_x: Literal[0, 1, 2]
    coordinate_y: Literal[0, 1, 2]

    def coordinates(self) -> tuple[int, int]:
        return self.coordinate_x, self.coordinate_y


# Response schemas
class MatchResponse(BaseModel):
    match_id: PositiveInt


class MoveResponse(BaseModel):
    id: PositiveInt
    match_id: PositiveInt
    user_id: PositiveInt
    coordinate_x: Literal[0, 1, 2]
    coordinate_y: Literal[0, 1, 2]
    winner_id: PositiveInt | None = None


class StatusResponse(BaseModel):
    match_id: PositiveInt
    user_x_id: PositiveInt
    user_o_id: PositiveInt
    user_turn: PositiveInt | None = None
    user_x_coordinates: list[list[Literal[0, 1, 2]]] = Field(default_factory=list)
    user_o_coordinates: list[list[Literal[0, 1, 2]]] = Field(default_factory=list)
    winner_id: PositiveInt | None = None
