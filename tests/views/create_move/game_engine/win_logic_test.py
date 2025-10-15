import pytest

from database.models import Match, Move, User
from src.game_engine import GameEngine


@pytest.mark.parametrize(
    "moves_data",
    [
        # vertical left
        [
            {"user_id": 1, "x": 0, "y": 0, "order": 1},
            {"user_id": 2, "x": 1, "y": 1, "order": 2},
            {"user_id": 1, "x": 0, "y": 1, "order": 3},
            {"user_id": 2, "x": 1, "y": 2, "order": 4},
            {"user_id": 1, "x": 0, "y": 2, "order": 5},
        ],
        # vertical middle
        [
            {"user_id": 1, "x": 1, "y": 0, "order": 1},
            {"user_id": 2, "x": 0, "y": 0, "order": 2},
            {"user_id": 1, "x": 1, "y": 1, "order": 3},
            {"user_id": 2, "x": 2, "y": 2, "order": 4},
            {"user_id": 1, "x": 1, "y": 2, "order": 5},
        ],
        # vertical right
        [
            {"user_id": 1, "x": 2, "y": 0, "order": 1},
            {"user_id": 2, "x": 0, "y": 0, "order": 2},
            {"user_id": 1, "x": 2, "y": 1, "order": 3},
            {"user_id": 2, "x": 0, "y": 2, "order": 4},
            {"user_id": 1, "x": 2, "y": 2, "order": 5},
        ],
        # horizontal top
        [
            {"user_id": 1, "x": 0, "y": 0, "order": 1},
            {"user_id": 2, "x": 1, "y": 1, "order": 2},
            {"user_id": 1, "x": 1, "y": 0, "order": 3},
            {"user_id": 2, "x": 2, "y": 1, "order": 4},
            {"user_id": 1, "x": 2, "y": 0, "order": 5},
        ],
        # horizontal middle
        [
            {"user_id": 1, "x": 0, "y": 1, "order": 1},
            {"user_id": 2, "x": 0, "y": 0, "order": 2},
            {"user_id": 1, "x": 1, "y": 1, "order": 3},
            {"user_id": 2, "x": 2, "y": 2, "order": 4},
            {"user_id": 1, "x": 2, "y": 1, "order": 5},
        ],
        # horizontal bottom
        [
            {"user_id": 1, "x": 0, "y": 2, "order": 1},
            {"user_id": 2, "x": 1, "y": 1, "order": 2},
            {"user_id": 1, "x": 1, "y": 2, "order": 3},
            {"user_id": 2, "x": 2, "y": 1, "order": 4},
            {"user_id": 1, "x": 2, "y": 2, "order": 5},
        ],
        # diagonal top-left to bottom-right
        [
            {"user_id": 1, "x": 0, "y": 0, "order": 1},
            {"user_id": 2, "x": 0, "y": 1, "order": 2},
            {"user_id": 1, "x": 1, "y": 1, "order": 3},
            {"user_id": 2, "x": 2, "y": 1, "order": 4},
            {"user_id": 1, "x": 2, "y": 2, "order": 5},
        ],
        # diagonal top-right to bottom-left
        [
            {"user_id": 1, "x": 2, "y": 0, "order": 1},
            {"user_id": 2, "x": 0, "y": 0, "order": 2},
            {"user_id": 1, "x": 1, "y": 1, "order": 3},
            {"user_id": 2, "x": 0, "y": 1, "order": 4},
            {"user_id": 1, "x": 0, "y": 2, "order": 5},
        ],
    ],
)
def test_x_win_logic(moves_data):
    user_x = User(name="UserX", password="password1")
    user_x.id = 1
    user_o = User(name="UserO", password="password2")
    user_o.id = 2

    match = Match(user_x_id=user_x.id, user_o_id=user_o.id, winner_id=None)
    match.id = 200

    moves = [
        Move(
            match_id=match.id,
            user_id=move_data["user_id"],
            coordinate_x=move_data["x"],
            coordinate_y=move_data["y"],
            move_order=move_data["order"],
        )
        for move_data in moves_data
    ]

    game_engine = GameEngine(match, moves=moves)

    assert game_engine.winner_id(moves=moves) == 1


@pytest.mark.parametrize(
    "moves_data",
    [
        # vertical left
        [
            {"user_id": 1, "x": 2, "y": 2, "order": 1},
            {"user_id": 2, "x": 0, "y": 0, "order": 2},
            {"user_id": 1, "x": 1, "y": 1, "order": 3},
            {"user_id": 2, "x": 0, "y": 1, "order": 4},
            {"user_id": 1, "x": 1, "y": 2, "order": 5},
            {"user_id": 2, "x": 0, "y": 2, "order": 6},
        ],
        # vertical middle
        [
            {"user_id": 1, "x": 0, "y": 1, "order": 1},
            {"user_id": 2, "x": 1, "y": 0, "order": 2},
            {"user_id": 1, "x": 0, "y": 0, "order": 3},
            {"user_id": 2, "x": 1, "y": 1, "order": 4},
            {"user_id": 1, "x": 2, "y": 2, "order": 5},
            {"user_id": 2, "x": 1, "y": 2, "order": 6},
        ],
        # vertical right
        [
            {"user_id": 1, "x": 1, "y": 1, "order": 1},
            {"user_id": 2, "x": 2, "y": 0, "order": 2},
            {"user_id": 1, "x": 0, "y": 0, "order": 3},
            {"user_id": 2, "x": 2, "y": 1, "order": 4},
            {"user_id": 1, "x": 0, "y": 2, "order": 5},
            {"user_id": 2, "x": 2, "y": 2, "order": 6},
        ],
        # horizontal top
        [
            {"user_id": 1, "x": 0, "y": 2, "order": 1},
            {"user_id": 2, "x": 0, "y": 0, "order": 2},
            {"user_id": 1, "x": 1, "y": 1, "order": 3},
            {"user_id": 2, "x": 1, "y": 0, "order": 4},
            {"user_id": 1, "x": 2, "y": 1, "order": 5},
            {"user_id": 2, "x": 2, "y": 0, "order": 6},
        ],
        # horizontal middle
        [
            {"user_id": 1, "x": 2, "y": 0, "order": 1},
            {"user_id": 2, "x": 0, "y": 1, "order": 2},
            {"user_id": 1, "x": 0, "y": 0, "order": 3},
            {"user_id": 2, "x": 1, "y": 1, "order": 4},
            {"user_id": 1, "x": 2, "y": 2, "order": 5},
            {"user_id": 2, "x": 2, "y": 1, "order": 6},
        ],
        # horizontal bottom
        [
            {"user_id": 1, "x": 0, "y": 0, "order": 1},
            {"user_id": 2, "x": 0, "y": 2, "order": 2},
            {"user_id": 1, "x": 1, "y": 1, "order": 3},
            {"user_id": 2, "x": 1, "y": 2, "order": 4},
            {"user_id": 1, "x": 2, "y": 1, "order": 5},
            {"user_id": 2, "x": 2, "y": 2, "order": 6},
        ],
        # diagonal top-left to bottom-right
        [
            {"user_id": 1, "x": 0, "y": 2, "order": 1},
            {"user_id": 2, "x": 0, "y": 0, "order": 2},
            {"user_id": 1, "x": 0, "y": 1, "order": 3},
            {"user_id": 2, "x": 1, "y": 1, "order": 4},
            {"user_id": 1, "x": 2, "y": 1, "order": 5},
            {"user_id": 2, "x": 2, "y": 2, "order": 6},
        ],
        # diagonal top-right to bottom-left
        [
            {"user_id": 1, "x": 2, "y": 2, "order": 1},
            {"user_id": 2, "x": 2, "y": 0, "order": 2},
            {"user_id": 1, "x": 0, "y": 0, "order": 3},
            {"user_id": 2, "x": 1, "y": 1, "order": 4},
            {"user_id": 1, "x": 0, "y": 1, "order": 5},
            {"user_id": 2, "x": 0, "y": 2, "order": 6},
        ],
    ],
)
def test_o_win_logic(moves_data):
    user_x = User(name="UserX", password="password1")
    user_x.id = 1
    user_o = User(name="UserO", password="password2")
    user_o.id = 2

    match = Match(user_x_id=user_x.id, user_o_id=user_o.id, winner_id=None)
    match.id = 200

    moves = [
        Move(
            match_id=match.id,
            user_id=move_data["user_id"],
            coordinate_x=move_data["x"],
            coordinate_y=move_data["y"],
            move_order=move_data["order"],
        )
        for move_data in moves_data
    ]

    game_engine = GameEngine(match, moves=moves)

    assert game_engine.winner_id(moves=moves) == 2
