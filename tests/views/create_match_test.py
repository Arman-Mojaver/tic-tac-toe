import pytest

from database.models import Match, User


@pytest.fixture(autouse=True)
def clear_users(session):
    yield
    session.query(Match).delete()
    session.query(User).delete()
    session.commit()


def test_create_match_nonexistent_user_x_raises_error(create_user, fake_id, client):
    user_o = create_user()
    response = client.post("/create", json={"user_x_id": fake_id, "user_o_id": user_o.id})
    assert response.status_code == 404
    assert response.json() == {"error": f"User not found. ID {fake_id}"}


def test_create_match_nonexistent_user_o_raises_error(create_user, fake_id, client):
    user_x = create_user()
    response = client.post("/create", json={"user_x_id": user_x.id, "user_o_id": fake_id})
    assert response.status_code == 404
    assert response.json() == {"error": f"User not found. ID {fake_id}"}


def test_create_match_with_same_user_raises_error(create_user, client):
    user = create_user()
    response = client.post("/create", json={"user_x_id": user.id, "user_o_id": user.id})
    assert response.status_code == 422
    assert response.json() == {"error": f"User ids can not be the same. ID: {user.id}"}


def test_successful(create_user, client, session):
    user_x = create_user(name="UserX")
    user_o = create_user(name="UserO")
    response = client.post(
        "/create",
        json={"user_x_id": user_x.id, "user_o_id": user_o.id},
    )
    assert response.status_code == 200
    match = session.query(Match).one_or_none()
    assert response.json() == {"match_id": match.id}
