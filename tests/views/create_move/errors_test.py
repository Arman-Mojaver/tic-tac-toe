def test_nonexistent_user_raises_error(
    create_match,
    fake_id,
    client,
):
    match = create_match()
    response = client.post(
        "/move",
        json={
            "match_id": match.id,
            "user_id": fake_id,
            "coordinate_x": 1,
            "coordinate_y": 2,
        },
    )
    assert response.status_code == 404
    assert response.json() == {"error": f"User not found. ID: {fake_id}"}


def test_nonexistent_match_raises_error(
    create_user,
    fake_id,
    client,
):
    user = create_user()
    response = client.post(
        "/move",
        json={
            "match_id": fake_id,
            "user_id": user.id,
            "coordinate_x": 1,
            "coordinate_y": 2,
        },
    )
    assert response.status_code == 404
    assert response.json() == {"error": f"Match not found. ID: {fake_id}"}


def test_user_does_not_belong_to_match_raises_error(
    create_user,
    create_match,
    fake_id,
    client,
):
    user = create_user()
    match = create_match()
    response = client.post(
        "/move",
        json={
            "match_id": match.id,
            "user_id": user.id,
            "coordinate_x": 1,
            "coordinate_y": 2,
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "error": f"User does not belong to match. User ID: {user.id}, Match ID: {match.id}"  # noqa: E501
    }


def test_finished_game_raises_error(
    create_user,
    create_match,
    fake_id,
    client,
):
    user_x = create_user()
    user_o = create_user()

    match = create_match(user_x=user_x, user_o=user_o, winner=user_x)

    # User x
    response = client.post(
        "/move",
        json={
            "match_id": match.id,
            "user_id": user_x.id,
            "coordinate_x": 1,
            "coordinate_y": 2,
        },
    )
    assert response.status_code == 409
    assert response.json() == {
        "error": f"The game has already finished. The winner is: {user_x.id}"
    }

    # User o
    response = client.post(
        "/move",
        json={
            "match_id": match.id,
            "user_id": user_o.id,
            "coordinate_x": 1,
            "coordinate_y": 2,
        },
    )
    assert response.status_code == 409
    assert response.json() == {
        "error": f"The game has already finished. The winner is: {user_x.id}"
    }


def test_invalid_coordinates_raises_error(
    create_user,
    create_match,
    fake_id,
    client,
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
            "coordinate_y": 3,
        },
    )
    assert response.status_code == 422


def test_finished_game_without_winner_with_move_raises_error(
    create_user,
    create_match,
    create_move,
    fake_id,
    client,
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
    create_move(match=match, user=match.user_o, x=2, y=2, order=8)
    create_move(match=match, user=match.user_x, x=2, y=1, order=9)

    response = client.post(
        "/move",
        json={
            "match_id": match.id,
            "user_id": user_o.id,
            "coordinate_x": 2,
            "coordinate_y": 2,
        },
    )
    assert response.status_code == 409
    assert response.json() == {"error": "The game has already finished without a winner. You can not make a move"}  # noqa: E501


def test_occupied_coordinates_raises_error(
    create_user,
    create_match,
    create_move,
    fake_id,
    client,
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
            "coordinate_x": 1,
            "coordinate_y": 1,
        },
    )
    assert response.status_code == 409
    assert response.json() == {
        "error": "Square already occupied. coordinate_x: 1, coordinate_y: 1"
    }


def test_invalid_turn_user_x_raises_error(
    create_user,
    create_match,
    create_move,
    fake_id,
    client,
):
    user_x = create_user()
    user_o = create_user()

    match = create_match(user_x=user_x, user_o=user_o)
    create_move(match=match, user=user_x, x=1, y=1, order=1)

    response = client.post(
        "/move",
        json={
            "match_id": match.id,
            "user_id": user_x.id,
            "coordinate_x": 1,
            "coordinate_y": 2,
        },
    )
    assert response.status_code == 409
    assert response.json() == {
        "error": f"Invalid turn. It is not the turn of user_id: {user_x.id}"
    }


def test_invalid_turn_user_o_raises_error(
    create_user,
    create_match,
    create_move,
    fake_id,
    client,
):
    user_x = create_user()
    user_o = create_user()

    match = create_match(user_x=user_x, user_o=user_o)
    create_move(match=match, user=user_x, x=1, y=1, order=1)
    create_move(match=match, user=user_o, x=1, y=2, order=2)

    response = client.post(
        "/move",
        json={
            "match_id": match.id,
            "user_id": user_o.id,
            "coordinate_x": 2,
            "coordinate_y": 2,
        },
    )
    assert response.status_code == 409
    assert response.json() == {
        "error": f"Invalid turn. It is not the turn of user_id: {user_o.id}"
    }
