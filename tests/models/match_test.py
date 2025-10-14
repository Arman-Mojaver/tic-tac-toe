import pytest

from database.models import Match, User


@pytest.fixture(autouse=True)
def clear_matches(session):
    yield
    session.query(Match).delete()
    session.query(User).delete()
    session.commit()


def test_create_match(session, create_match):
    match = create_match()

    db_match = session.query(Match).filter_by(id=match.id).first()
    assert db_match is not None
    assert match.id == db_match.id
    assert match.user_x_id == db_match.user_x_id
    assert match.user_o_id == db_match.user_o_id
    assert db_match.winner_id is None


def test_update_match_winner(session, create_match):
    match = create_match()

    match.winner_id = match.user_x_id
    session.commit()

    db_match = session.query(Match).filter_by(id=match.id).one()
    assert db_match.winner_id == match.user_x_id


def test_delete_match(session, create_match):
    match = create_match()

    session.delete(match)
    session.commit()

    db_match = session.query(Match).filter_by(id=match.id).one_or_none()
    assert db_match is None


def test_serialize_rules(create_match):
    match = create_match()

    serialized = match.to_dict()
    assert serialized["id"] == match.id
    assert serialized["user_x_id"] == match.user_x_id
    assert serialized["user_o_id"] == match.user_o_id
    assert "winner_id" in serialized
