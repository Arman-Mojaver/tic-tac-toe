from database.models import Move


def test_successful_initial_move(  # noqa: PLR0913
    create_user,
    create_match,
    create_move,
    fake_id,
    client,
    session,
):
    user_x = create_user()
    user_o = create_user()

    match = create_match(user_x=user_x, user_o=user_o)

    response = client.post(
        "/move",
        json={
            "match_id": match.id,
            "user_id": user_x.id,
            "coordinate_x": 1,
            "coordinate_y": 1,
        },
    )
    assert response.status_code == 200
    move = session.query(Move).filter_by(match_id=match.id).one_or_none()
    assert response.json() == {
        "data": {
            "id": move.id,
            "match_id": match.id,
            "user_id": user_x.id,
            "coordinate_x": 1,
            "coordinate_y": 1,
            "winner_id": None,
        }
    }
    assert not move.match.winner_id


def test_successful_move(  # noqa: PLR0913
    create_user,
    create_match,
    create_move,
    fake_id,
    client,
    session,
):
    user_x = create_user()
    user_o = create_user()

    match = create_match(user_x=user_x, user_o=user_o)
    create_move(match=match, user=user_x, x=1, y=1, order=1)

    response = client.post(
        "/move",
        json={
            "match_id": match.id,
            "user_id": user_o.id,
            "coordinate_x": 2,
            "coordinate_y": 2,
        },
    )
    assert response.status_code == 200
    move = session.query(Move).filter_by(match_id=match.id, move_order=2).one_or_none()
    assert response.json() == {
        "data": {
            "id": move.id,
            "match_id": match.id,
            "user_id": user_o.id,
            "coordinate_x": 2,
            "coordinate_y": 2,
            "winner_id": None,
        }
    }
    assert not move.match.winner_id


def test_successful_move_ends_the_game_without_winner(  # noqa: PLR0913
    create_user,
    create_match,
    create_move,
    fake_id,
    client,
    session,
):
    user_x = create_user()
    user_o = create_user()

    match = create_match(user_x=user_x, user_o=user_o)
    create_move(match=match, user=match.user_x, x=1, y=1, order=1)
    create_move(match=match, user=match.user_o, x=0, y=0, order=2)
    create_move(match=match, user=match.user_x, x=1, y=2, order=3)
    create_move(match=match, user=match.user_o, x=1, y=0, order=4)
    create_move(match=match, user=match.user_x, x=2, y=0, order=5)
    create_move(match=match, user=match.user_o, x=0, y=2, order=6)
    create_move(match=match, user=match.user_x, x=0, y=1, order=7)
    create_move(match=match, user=match.user_o, x=2, y=1, order=8)

    response = client.post(
        "/move",
        json={
            "match_id": match.id,
            "user_id": user_x.id,
            "coordinate_x": 2,
            "coordinate_y": 2,
        },
    )
    assert response.status_code == 200
    move = session.query(Move).filter_by(match_id=match.id, move_order=9).one_or_none()
    assert response.json() == {
        "data": {
            "id": move.id,
            "match_id": match.id,
            "user_id": user_x.id,
            "coordinate_x": 2,
            "coordinate_y": 2,
            "winner_id": None,
        }
    }
    assert not move.match.winner_id
