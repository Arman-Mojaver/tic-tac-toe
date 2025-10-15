from __future__ import annotations

from database import session
from database.models import Match, Move
from database.models.move import MoveList
from src.schemas import StatusResponse


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

    def status(self) -> StatusResponse:
        return StatusResponse(
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

        moves = sorted([*self.moves, move], key=lambda m: m.move_order)
        user_x_moves = [move for move in moves if move.user_id == self.user_x_id]
        user_o_moves = [move for move in moves if move.user_id == self.user_o_id]

        winner_id = self.winner_id(user_x_moves=user_x_moves, user_o_moves=user_o_moves)
        self.match.winner_id = winner_id
        session.add(self.match)
        return move

    def winner_id(self, user_x_moves: list[Move], user_o_moves: list[Move]) -> int | None:
        user_x_coordinates = set(MoveList(user_x_moves).coordinates())
        user_o_coordinates = set(MoveList(user_o_moves).coordinates())

        if any(
            winning_coordinates.issubset(user_x_coordinates)
            for winning_coordinates in self.ALL_WINNING_COORDINATES
        ):
            return user_x_moves[-1].user_id

        if any(
            winning_coordinates.issubset(user_o_coordinates)
            for winning_coordinates in self.ALL_WINNING_COORDINATES
        ):
            return user_o_moves[-1].user_id

        return None
