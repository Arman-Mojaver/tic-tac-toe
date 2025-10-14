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
