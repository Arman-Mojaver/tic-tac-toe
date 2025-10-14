import pytest

from database.models import Match, Move, User


@pytest.fixture(autouse=True)
def clear_moves(session):
    yield
    session.query(Move).delete()
    session.query(Match).delete()
    session.query(User).delete()
    session.commit()


@pytest.fixture
def move(create_move, create_match):
    match = create_match()
    return create_move(match=match, user=match.user_x, x=2, y=3, order=1)


def test_create_move(session, move):
    db_move = session.query(Move).filter_by(id=move.id).first()
    assert db_move is not None
    assert move.id == db_move.id
    assert move.match_id == db_move.match_id
    assert move.user_id == db_move.user_id
    assert db_move.coordinate_x == 2
    assert db_move.coordinate_y == 3
    assert db_move.move_order == 1


def test_update_move_order(session, move):
    move.move_order = 2
    session.commit()

    db_move = session.query(Move).filter_by(id=move.id).one()
    assert db_move.move_order == 2


def test_delete_move(session, move):
    session.delete(move)
    session.commit()

    db_move = session.query(Move).filter_by(id=move.id).one_or_none()
    assert db_move is None


def test_serialize_rules(move):
    serialized = move.to_dict()
    assert serialized["id"] == move.id
    assert serialized["match_id"] == move.match_id
    assert serialized["user_id"] == move.user_id
