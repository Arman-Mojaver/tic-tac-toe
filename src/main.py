from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from database import session
from src.errors import (
    GameFinishedError,
    InvalidTurnError,
    MatchNotFoundError,
    MismatchError,
    OccupiedSquareError,
    SameUserError,
    UserNotFoundError,
)
from src.schemas import MatchUsers, MoveData
from src.views.create_match_view import create_match_view
from src.views.create_move_view import create_move_view
from src.views.get_status_view import get_status_view

app = FastAPI(title="tictactoe")


@app.get("/health", status_code=HTTPStatus.OK)
def health_check() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})


@app.post("/create")
def create_match(match_users: MatchUsers) -> JSONResponse:
    try:
        match = create_match_view(match_users=match_users)
    except UserNotFoundError as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=HTTPStatus.NOT_FOUND,
        )
    except SameUserError as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    return JSONResponse(content={"match_id": match.id})


@app.get("/status")
def get_status(match_id: int) -> JSONResponse:
    try:
        game_status = get_status_view(match_id=match_id)
    except MatchNotFoundError as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=HTTPStatus.NOT_FOUND,
        )

    return JSONResponse(
        content={"data": game_status.model_dump()},
        status_code=HTTPStatus.OK,
    )


@app.post("/move")
def create_move(move_data: MoveData) -> JSONResponse:
    try:
        move = create_move_view(move_data=move_data)
    except (UserNotFoundError, MatchNotFoundError, MismatchError) as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=HTTPStatus.NOT_FOUND,
        )
    except (GameFinishedError, OccupiedSquareError, InvalidTurnError) as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=HTTPStatus.CONFLICT,
        )

    session.commit()

    return JSONResponse(
        content={
            "data": {
                "id": move.id,
                "match_id": move.match.id,
                "user_id": move_data.user_id,
                "coordinate_x": move_data.coordinate_x,
                "coordinate_y": move_data.coordinate_y,
                "winner_id": move.match.winner_id,
            }
        },
        status_code=HTTPStatus.OK,
    )
