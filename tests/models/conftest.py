import pytest

from database.models import Match, Move, User


@pytest.fixture
def create_match(session, create_user):
    def _create_match(x_name="PlayerX", o_name="PlayerO", winner=None):
        user_x = create_user(name=x_name, password="secret")
        user_o = create_user(name=o_name, password="secret")
        match = Match(user_x_id=user_x.id, user_o_id=user_o.id, winner_id=winner)
        session.add(match)
        session.commit()
        session.refresh(match)
        return match

    return _create_match


@pytest.fixture
def create_move(session, create_match):
    def _create_move(match: Match, user: User, x: int = 0, y: int = 1, order: int = 1):
        move = Move(
            match_id=match.id,
            user_id=user.id,
            coordinate_x=x,
            coordinate_y=y,
            move_order=order,
        )
        session.add(move)
        session.commit()
        session.refresh(move)
        return move

    return _create_move
