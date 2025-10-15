def test_x_won(client, create_match, create_move, create_user):
    user_x = create_user()
    user_o = create_user()

    match = create_match(user_x=user_x, user_o=user_o, winner=user_x)
    create_move(match=match, user=match.user_x, x=0, y=0, order=1)
    create_move(match=match, user=match.user_o, x=1, y=0, order=2)
    create_move(match=match, user=match.user_x, x=0, y=1, order=3)
    create_move(match=match, user=match.user_o, x=1, y=1, order=4)
    create_move(match=match, user=match.user_x, x=0, y=2, order=5)

    response = client.get("/status", params={"match_id": match.id})
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "match_id": match.id,
            "user_x_id": match.user_x_id,
            "user_o_id": match.user_o_id,
            "user_turn": None,
            "user_x_coordinates": [[0, 0], [0, 1], [0, 2]],
            "user_o_coordinates": [[1, 0], [1, 1]],
            "winner_id": match.user_x_id,
        }
    }


def test_o_won(client, create_match, create_move, create_user):
    user_x = create_user()
    user_o = create_user()

    match = create_match(user_x=user_x, user_o=user_o, winner=user_o)
    create_move(match=match, user=match.user_x, x=0, y=0, order=1)
    create_move(match=match, user=match.user_o, x=1, y=0, order=2)
    create_move(match=match, user=match.user_x, x=0, y=1, order=3)
    create_move(match=match, user=match.user_o, x=1, y=1, order=4)
    create_move(match=match, user=match.user_x, x=2, y=2, order=5)
    create_move(match=match, user=match.user_o, x=1, y=2, order=6)

    response = client.get("/status", params={"match_id": match.id})
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "match_id": match.id,
            "user_x_id": match.user_x_id,
            "user_o_id": match.user_o_id,
            "user_turn": None,
            "user_x_coordinates": [[0, 0], [0, 1], [2, 2]],
            "user_o_coordinates": [[1, 0], [1, 1], [1, 2]],
            "winner_id": match.user_o_id,
        }
    }
