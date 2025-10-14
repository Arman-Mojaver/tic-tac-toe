import pytest

from database.models import User


@pytest.fixture
def create_user(session):
    def _create_user(name="TestUser", password="secret"):  # noqa: S107
        user = User(name=name, password=password)
        session.add(user)
        session.commit()
        return user
    return _create_user


@pytest.fixture(autouse=True)
def clear_users(session):
    session.query(User).delete()
    session.commit()



def test_create_user(session, create_user):
    user = create_user(name="Alice", password="secret")

    db_user = session.query(User).filter_by(name="Alice").first()
    assert user.id == db_user.id
    assert user.name == db_user.name



def test_update_user(session, create_user):
    user = create_user(name="Charlie", password="secret")

    user.name = "CharlieUpdated"
    session.commit()

    db_user = session.query(User).filter_by(id=user.id).one()
    assert db_user.name == "CharlieUpdated"


def test_delete_user(session, create_user):
    user = create_user(name="Dave", password="secret")

    session.delete(user)
    session.commit()

    db_user = session.query(User).filter_by(id=user.id).one_or_none()
    assert db_user is None


def test_serialize_rules(create_user):
    user = create_user(name="Eve", password="secret")

    assert user.to_dict() == {"id": user.id, "name": user.name}
