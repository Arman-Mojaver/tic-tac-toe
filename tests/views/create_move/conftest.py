import pytest

from database.models import Match, Move, User


@pytest.fixture(autouse=True)
def clear_data(session):
    yield
    session.query(Move).delete()
    session.query(Match).delete()
    session.query(User).delete()
    session.commit()
