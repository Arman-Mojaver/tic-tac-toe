def test_invalid_match_id_raises_error(client, fake_id):
    response = client.get("/status", params={"match_id": fake_id})
    assert response.status_code == 404
    assert response.json() == {"error": f"Match ID not found: {fake_id}"}


def test_initialized_game_returns_no_coordinates_and_user_x_turn(client, create_match):
    match = create_match()
    response = client.get("/status", params={"match_id": match.id})
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "match_id": match.id,
            "user_x_id": match.user_x_id,
            "user_o_id": match.user_o_id,
            "user_turn_id": match.user_x_id,
            "user_x_coordinates": [],
            "user_o_coordinates": [],
            "winner_id": None,
        }
    }
