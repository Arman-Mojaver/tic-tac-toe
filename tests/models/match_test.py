import pytest

from database.models import Match, User


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


@pytest.fixture(autouse=True)
def clear_matches(session):
    yield
    session.query(Match).delete()
    session.query(User).delete()
    session.commit()


def test_create_match(session, create_match):
    match = create_match(x_name="AliceX", o_name="BobO")

    db_match = session.query(Match).filter_by(id=match.id).first()
    assert db_match is not None
    assert match.id == db_match.id
    assert match.user_x_id == db_match.user_x_id
    assert match.user_o_id == db_match.user_o_id
    assert db_match.winner_id is None


def test_update_match_winner(session, create_match):
    match = create_match(x_name="CharlieX", o_name="DanaO")

    match.winner_id = match.user_x_id
    session.commit()

    db_match = session.query(Match).filter_by(id=match.id).one()
    assert db_match.winner_id == match.user_x_id


def test_delete_match(session, create_match):
    match = create_match(x_name="EddieX", o_name="FionaO")

    session.delete(match)
    session.commit()

    db_match = session.query(Match).filter_by(id=match.id).one_or_none()
    assert db_match is None


def test_serialize_rules(create_match):
    match = create_match(x_name="GabeX", o_name="HanaO")

    serialized = match.to_dict()
    assert serialized["id"] == match.id
    assert serialized["user_x_id"] == match.user_x_id
    assert serialized["user_o_id"] == match.user_o_id
    assert "winner_id" in serialized
