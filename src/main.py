from fastapi import FastAPI
from fastapi.responses import JSONResponse

from database import session
from database.models import Match, User
from database.models.move import MoveList
from src.game_engine import GameEngine
from src.schemas import MatchUsers, MoveData

app = FastAPI(title="tictactoe")


@app.get("/health", status_code=200)
def health_check() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})


@app.post("/create")
def create_match(match_users: MatchUsers) -> JSONResponse:
    user_x = session.query(User).filter_by(id=match_users.user_x_id).one_or_none()
    if not user_x:
        return JSONResponse(
            content={"error": f"User not found. ID {match_users.user_x_id}"},
            status_code=404,
        )

    user_o = session.query(User).filter_by(id=match_users.user_o_id).one_or_none()
    if not user_o:
        return JSONResponse(
            content={"error": f"User not found. ID {match_users.user_o_id}"},
            status_code=404,
        )

    if user_x.id == user_o.id:
        return JSONResponse(
            content={"error": f"User ids can not be the same. ID: {user_x.id}"},
            status_code=422,
        )

    match = Match(user_x_id=user_x.id, user_o_id=user_o.id)
    session.add(match)
    session.commit()
    session.refresh(match)

    return JSONResponse(content={"match_id": match.id})


@app.get("/status")
def get_status(match_id: int) -> JSONResponse:
    match = session.query(Match).filter_by(id=match_id).one_or_none()
    if not match:
        return JSONResponse(
            content={"error": f"Match ID not found: {match_id}"},
            status_code=404,
        )

    game_engine = GameEngine(match=match, moves=match.moves)
    status = game_engine.status()

    return JSONResponse(
        content={"data": status.model_dump()},
        status_code=200,
    )


@app.post("/move")
def create_move(move_data: MoveData) -> JSONResponse:  # noqa: PLR0911
    user = session.query(User).filter_by(id=move_data.user_id).one_or_none()
    if not user:
        return JSONResponse(
            content={"error": f"User not found. ID: {move_data.user_id}"},
            status_code=404,
        )

    match = session.query(Match).filter_by(id=move_data.match_id).one_or_none()
    if not match:
        return JSONResponse(
            content={"error": f"Match not found. ID: {move_data.match_id}"},
            status_code=404,
        )

    if move_data.user_id not in match.user_ids():
        return JSONResponse(
            content={
                "error": f"User does not belong to match. User ID: {user.id}, Match ID: {match.id}"  # noqa: E501
            },
            status_code=404,
        )

    if match.winner_id:
        return JSONResponse(
            content={
                "error": f"The game has already finished. The winner is: {match.winner_id}"  # noqa: E501
            },
            status_code=409,
        )

    if len(match.moves) == GameEngine.MAX_MOVE_COUNT and not match.winner_id:
        return JSONResponse(
            content={
                "error": "The game has already finished without a winner. You can not make a move"  # noqa: E501
            },
            status_code=409,
        )

    if move_data.coordinates() in MoveList(match.moves).coordinates():
        return JSONResponse(
            content={
                "error": f"Square already occupied. coordinate_x: {move_data.coordinate_x}, coordinate_y: {move_data.coordinate_y}"  # noqa: E501
            },
            status_code=409,
        )



    game_engine = GameEngine(match=match, moves=match.moves)

    if game_engine.user_turn() != move_data.user_id:
        return JSONResponse(
            content={
                "error": f"Invalid turn. It is not the turn of user_id: {move_data.user_id}"  # noqa: E501
            },
            status_code=409,
        )

    move = game_engine.create_move(
        user_id=move_data.user_id,
        coordinate_x=move_data.coordinate_x,
        coordinate_y=move_data.coordinate_y,
    )

    session.commit()

    return JSONResponse(
        content={
            "data": {
                "id": move.id,
                "match_id": match.id,
                "user_id": move_data.user_id,
                "coordinate_x": move_data.coordinate_x,
                "coordinate_y": move_data.coordinate_y,
            }
        },
        status_code=200,
    )
