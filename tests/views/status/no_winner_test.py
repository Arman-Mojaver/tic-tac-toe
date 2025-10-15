def test_in_progress_game_with_one_move_returns_status(client, create_match, create_move):
    match = create_match()
    create_move(match=match, user=match.user_x, x=1, y=1, order=1)
    response = client.get("/status", params={"match_id": match.id})
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "match_id": match.id,
            "user_x_id": match.user_x_id,
            "user_o_id": match.user_o_id,
            "user_turn_id": match.user_o_id,
            "user_x_coordinates": [[1, 1]],
            "user_o_coordinates": [],
            "winner_id": None,
        }
    }


def test_in_progress_game_with_two_moves_returns_status(
    client,
    create_match,
    create_move,
):
    match = create_match()
    create_move(match=match, user=match.user_x, x=1, y=1, order=1)
    create_move(match=match, user=match.user_o, x=0, y=0, order=2)
    response = client.get("/status", params={"match_id": match.id})
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "match_id": match.id,
            "user_x_id": match.user_x_id,
            "user_o_id": match.user_o_id,
            "user_turn_id": match.user_x_id,
            "user_x_coordinates": [[1, 1]],
            "user_o_coordinates": [[0, 0]],
            "winner_id": None,
        }
    }


def test_in_progress_game_with_three_moves_returns_status(
    client,
    create_match,
    create_move,
):
    match = create_match()
    create_move(match=match, user=match.user_x, x=1, y=1, order=1)
    create_move(match=match, user=match.user_o, x=0, y=0, order=2)
    create_move(match=match, user=match.user_x, x=1, y=2, order=3)
    response = client.get("/status", params={"match_id": match.id})
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "match_id": match.id,
            "user_x_id": match.user_x_id,
            "user_o_id": match.user_o_id,
            "user_turn_id": match.user_o_id,
            "user_x_coordinates": [[1, 1], [1, 2]],
            "user_o_coordinates": [[0, 0]],
            "winner_id": None,
        }
    }


def test_in_progress_game_with_four_moves_returns_status(
    client,
    create_match,
    create_move,
):
    match = create_match()
    create_move(match=match, user=match.user_x, x=1, y=1, order=1)
    create_move(match=match, user=match.user_o, x=0, y=0, order=2)
    create_move(match=match, user=match.user_x, x=1, y=2, order=3)
    create_move(match=match, user=match.user_o, x=1, y=0, order=4)
    response = client.get("/status", params={"match_id": match.id})
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "match_id": match.id,
            "user_x_id": match.user_x_id,
            "user_o_id": match.user_o_id,
            "user_turn_id": match.user_x_id,
            "user_x_coordinates": [[1, 1], [1, 2]],
            "user_o_coordinates": [[0, 0], [1, 0]],
            "winner_id": None,
        }
    }


def test_in_progress_game_with_five_moves_returns_status(
    client,
    create_match,
    create_move,
):
    match = create_match()
    create_move(match=match, user=match.user_x, x=1, y=1, order=1)
    create_move(match=match, user=match.user_o, x=0, y=0, order=2)
    create_move(match=match, user=match.user_x, x=1, y=2, order=3)
    create_move(match=match, user=match.user_o, x=1, y=0, order=4)
    create_move(match=match, user=match.user_x, x=2, y=0, order=5)
    response = client.get("/status", params={"match_id": match.id})
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "match_id": match.id,
            "user_x_id": match.user_x_id,
            "user_o_id": match.user_o_id,
            "user_turn_id": match.user_o_id,
            "user_x_coordinates": [[1, 1], [1, 2], [2, 0]],
            "user_o_coordinates": [[0, 0], [1, 0]],
            "winner_id": None,
        }
    }


def test_in_progress_game_with_six_moves_returns_status(
    client,
    create_match,
    create_move,
):
    match = create_match()
    create_move(match=match, user=match.user_x, x=1, y=1, order=1)
    create_move(match=match, user=match.user_o, x=0, y=0, order=2)
    create_move(match=match, user=match.user_x, x=1, y=2, order=3)
    create_move(match=match, user=match.user_o, x=1, y=0, order=4)
    create_move(match=match, user=match.user_x, x=2, y=0, order=5)
    create_move(match=match, user=match.user_o, x=0, y=2, order=6)
    response = client.get("/status", params={"match_id": match.id})
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "match_id": match.id,
            "user_x_id": match.user_x_id,
            "user_o_id": match.user_o_id,
            "user_turn_id": match.user_x_id,
            "user_x_coordinates": [[1, 1], [1, 2], [2, 0]],
            "user_o_coordinates": [[0, 0], [1, 0], [0, 2]],
            "winner_id": None,
        }
    }


def test_in_progress_game_with_seven_moves_returns_status(
    client,
    create_match,
    create_move,
):
    match = create_match()
    create_move(match=match, user=match.user_x, x=1, y=1, order=1)
    create_move(match=match, user=match.user_o, x=0, y=0, order=2)
    create_move(match=match, user=match.user_x, x=1, y=2, order=3)
    create_move(match=match, user=match.user_o, x=1, y=0, order=4)
    create_move(match=match, user=match.user_x, x=2, y=0, order=5)
    create_move(match=match, user=match.user_o, x=0, y=2, order=6)
    create_move(match=match, user=match.user_x, x=0, y=1, order=7)
    response = client.get("/status", params={"match_id": match.id})
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "match_id": match.id,
            "user_x_id": match.user_x_id,
            "user_o_id": match.user_o_id,
            "user_turn_id": match.user_o_id,
            "user_x_coordinates": [[1, 1], [1, 2], [2, 0], [0, 1]],
            "user_o_coordinates": [[0, 0], [1, 0], [0, 2]],
            "winner_id": None,
        }
    }


def test_in_progress_game_with_eight_moves_returns_status(
    client,
    create_match,
    create_move,
):
    match = create_match()
    create_move(match=match, user=match.user_x, x=1, y=1, order=1)
    create_move(match=match, user=match.user_o, x=0, y=0, order=2)
    create_move(match=match, user=match.user_x, x=1, y=2, order=3)
    create_move(match=match, user=match.user_o, x=1, y=0, order=4)
    create_move(match=match, user=match.user_x, x=2, y=0, order=5)
    create_move(match=match, user=match.user_o, x=0, y=2, order=6)
    create_move(match=match, user=match.user_x, x=0, y=1, order=7)
    create_move(match=match, user=match.user_o, x=2, y=2, order=8)
    response = client.get("/status", params={"match_id": match.id})
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "match_id": match.id,
            "user_x_id": match.user_x_id,
            "user_o_id": match.user_o_id,
            "user_turn_id": match.user_x_id,
            "user_x_coordinates": [[1, 1], [1, 2], [2, 0], [0, 1]],
            "user_o_coordinates": [[0, 0], [1, 0], [0, 2], [2, 2]],
            "winner_id": None,
        }
    }


def test_in_progress_game_with_nine_moves_returns_status(
    client,
    create_match,
    create_move,
):
    match = create_match()
    create_move(match=match, user=match.user_x, x=1, y=1, order=1)
    create_move(match=match, user=match.user_o, x=0, y=0, order=2)
    create_move(match=match, user=match.user_x, x=1, y=2, order=3)
    create_move(match=match, user=match.user_o, x=1, y=0, order=4)
    create_move(match=match, user=match.user_x, x=2, y=0, order=5)
    create_move(match=match, user=match.user_o, x=0, y=2, order=6)
    create_move(match=match, user=match.user_x, x=0, y=1, order=7)
    create_move(match=match, user=match.user_o, x=2, y=2, order=8)
    create_move(match=match, user=match.user_x, x=2, y=1, order=9)

    response = client.get("/status", params={"match_id": match.id})
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "match_id": match.id,
            "user_x_id": match.user_x_id,
            "user_o_id": match.user_o_id,
            "user_turn_id": None,
            "user_x_coordinates": [[1, 1], [1, 2], [2, 0], [0, 1], [2, 1]],
            "user_o_coordinates": [[0, 0], [1, 0], [0, 2], [2, 2]],
            "winner_id": None,
        }
    }
