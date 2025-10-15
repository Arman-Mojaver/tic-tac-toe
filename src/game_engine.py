from __future__ import annotations

from typing import TYPE_CHECKING

from database import session
from database.models import Move
from database.models.move import MoveList
from src.schemas import GameStatus

if TYPE_CHECKING:
    from database.models import Match


class GameEngine:
    MAX_MOVE_COUNT = 9
    ALL_WINNING_COORDINATES = (
        # Vertical wins
        {(0, 0), (0, 1), (0, 2)},
        {(1, 0), (1, 1), (1, 2)},
        {(2, 0), (2, 1), (2, 2)},
        # Horizontal wins
        {(0, 0), (1, 0), (2, 0)},
        {(0, 1), (1, 1), (2, 1)},
        {(0, 2), (1, 2), (2, 2)},
        # Diagonal wins
        {(0, 0), (1, 1), (2, 2)},
        {(2, 0), (1, 1), (0, 2)},
    )

    def __init__(self, match: Match, moves: list[Move]):
        self.match = match
        self.user_x_id: int = match.user_x_id
        self.user_o_id: int = match.user_o_id
        self.moves: list[Move] = moves

    def status(self) -> GameStatus:
        return GameStatus(
            match_id=self.match.id,
            user_x_id=self.user_x_id,
            user_o_id=self.user_o_id,
            user_turn=self.user_turn(),
            user_x_coordinates=self._user_coordinates(user_id=self.user_x_id),
            user_o_coordinates=self._user_coordinates(user_id=self.user_o_id),
            winner_id=self.match.winner_id,
        )

    def _user_coordinates(self, user_id: int) -> list[list[int, int]]:
        return [
            [move.coordinate_x, move.coordinate_y]
            for move in self.moves
            if move.user_id == user_id
        ]

    def user_turn(self) -> int | None:
        if len(self.moves) == self.MAX_MOVE_COUNT or self.match.winner_id:
            return None

        if not self.moves or self.moves[-1].user_id != self.user_x_id:
            return self.user_x_id

        return self.user_o_id

    def create_move(self, user_id: int, coordinate_x: int, coordinate_y: int) -> Move:
        current_move_order = self.moves[-1].move_order if self.moves else 1
        move = Move(
            match_id=self.match.id,
            user_id=user_id,
            coordinate_x=coordinate_x,
            coordinate_y=coordinate_y,
            move_order=current_move_order + 1,
        )
        session.add(move)
        return move

    def winner_id(self, moves: list[Move]) -> int | None:
        coordinates = set(MoveList(moves).coordinates())

        if any(
            winning_coordinates.issubset(coordinates)
            for winning_coordinates in self.ALL_WINNING_COORDINATES
        ):
            return moves[-1].user_id

        return None
