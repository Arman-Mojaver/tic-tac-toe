import pytest

from database.models import Match, Move, User
from src.game_engine import GameEngine


@pytest.mark.parametrize(
    "moves_data",
    [
        [],
        [{"user_id": 1, "x": 1, "y": 1, "order": 1}],
        [
            {"user_id": 1, "x": 1, "y": 1, "order": 1},
            {"user_id": 2, "x": 0, "y": 0, "order": 2},
        ],
        [
            {"user_id": 1, "x": 1, "y": 1, "order": 1},
            {"user_id": 2, "x": 0, "y": 0, "order": 2},
            {"user_id": 1, "x": 1, "y": 2, "order": 3},
        ],
        [
            {"user_id": 1, "x": 1, "y": 1, "order": 1},
            {"user_id": 2, "x": 0, "y": 0, "order": 2},
            {"user_id": 1, "x": 1, "y": 2, "order": 3},
            {"user_id": 2, "x": 1, "y": 0, "order": 4},
        ],
        [
            {"user_id": 1, "x": 1, "y": 1, "order": 1},
            {"user_id": 2, "x": 0, "y": 0, "order": 2},
            {"user_id": 1, "x": 1, "y": 2, "order": 3},
            {"user_id": 2, "x": 1, "y": 0, "order": 4},
            {"user_id": 1, "x": 2, "y": 0, "order": 5},
        ],
        [
            {"user_id": 1, "x": 1, "y": 1, "order": 1},
            {"user_id": 2, "x": 0, "y": 0, "order": 2},
            {"user_id": 1, "x": 1, "y": 2, "order": 3},
            {"user_id": 2, "x": 1, "y": 0, "order": 4},
            {"user_id": 1, "x": 2, "y": 0, "order": 5},
            {"user_id": 2, "x": 0, "y": 2, "order": 6},
        ],
        [
            {"user_id": 1, "x": 1, "y": 1, "order": 1},
            {"user_id": 2, "x": 0, "y": 0, "order": 2},
            {"user_id": 1, "x": 1, "y": 2, "order": 3},
            {"user_id": 2, "x": 1, "y": 0, "order": 4},
            {"user_id": 1, "x": 2, "y": 0, "order": 5},
            {"user_id": 2, "x": 0, "y": 2, "order": 6},
            {"user_id": 1, "x": 0, "y": 1, "order": 7},
        ],
        [
            {"user_id": 1, "x": 1, "y": 1, "order": 1},
            {"user_id": 2, "x": 0, "y": 0, "order": 2},
            {"user_id": 1, "x": 1, "y": 2, "order": 3},
            {"user_id": 2, "x": 1, "y": 0, "order": 4},
            {"user_id": 1, "x": 2, "y": 0, "order": 5},
            {"user_id": 2, "x": 0, "y": 2, "order": 6},
            {"user_id": 1, "x": 0, "y": 1, "order": 7},
            {"user_id": 2, "x": 2, "y": 2, "order": 8},
        ],
        [
            {"user_id": 1, "x": 1, "y": 1, "order": 1},
            {"user_id": 2, "x": 0, "y": 0, "order": 2},
            {"user_id": 1, "x": 1, "y": 2, "order": 3},
            {"user_id": 2, "x": 1, "y": 0, "order": 4},
            {"user_id": 1, "x": 2, "y": 0, "order": 5},
            {"user_id": 2, "x": 0, "y": 2, "order": 6},
            {"user_id": 1, "x": 0, "y": 1, "order": 7},
            {"user_id": 2, "x": 2, "y": 2, "order": 8},
            {"user_id": 1, "x": 2, "y": 1, "order": 9},
        ],
    ],
)
def test_no_win_logic(moves_data):
    user_x = User(name="UserX", password="password1")
    user_x.id = 1
    user_o = User(name="UserO", password="password2")
    user_o.id = 2

    match = Match(user_x_id=user_x.id, user_o_id=user_o.id, winner_id=None)

    moves = [
        Move(
            match_id=match.id, user_id=move_data["user_id"], move_order=move_data["order"]
        )
        for move_data in moves_data
    ]

    game_engine = GameEngine(match, moves=moves)

    assert game_engine.winner_id(moves=moves) is None
