from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from logger import log
from src.errors import (
    GameFinishedError,
    InvalidTurnError,
    MatchNotFoundError,
    MismatchError,
    OccupiedSquareError,
    SameUserError,
    UserNotFoundError,
)
from src.schemas import CreateMatchData, CreateMoveData
from src.views.create_match_view import create_match_view
from src.views.create_move_view import create_move_view
from src.views.get_status_view import get_status_view

app = FastAPI(title="tictactoe")


@app.get("/health", status_code=HTTPStatus.OK)
def health_check() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})


@app.post("/create")
def create_match(create_match_data: CreateMatchData) -> JSONResponse:
    try:
        match_response = create_match_view(create_match_data=create_match_data)
    except UserNotFoundError as e:
        log.error(f"{e!r}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=HTTPStatus.NOT_FOUND,
        )
    except SameUserError as e:
        log.error(f"{e!r}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        )
    except Exception as e:  # noqa: BLE001
        log.exception("Unexpected error: %s", e)
        return JSONResponse(..., status_code=500)

    log.info("Match created. ID: %s", match_response.match_id)
    return JSONResponse(content={"data": match_response.model_dump()})


@app.get("/status")
def get_status(match_id: int) -> JSONResponse:
    try:
        game_status = get_status_view(match_id=match_id)
    except MatchNotFoundError as e:
        log.error(f"{e!r}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=HTTPStatus.NOT_FOUND,
        )
    except Exception as e:  # noqa: BLE001
        log.exception("Unexpected error: %s", e)
        return JSONResponse(..., status_code=500)

    return JSONResponse(
        content={"data": game_status.model_dump()},
        status_code=HTTPStatus.OK,
    )


@app.post("/move")
def create_move(create_move_data: CreateMoveData) -> JSONResponse:
    try:
        move_response = create_move_view(create_move_data=create_move_data)
    except (UserNotFoundError, MatchNotFoundError, MismatchError) as e:
        log.error(f"{e!r}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=HTTPStatus.NOT_FOUND,
        )
    except (GameFinishedError, OccupiedSquareError, InvalidTurnError) as e:
        log.error(f"{e!r}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=HTTPStatus.CONFLICT,
        )
    except Exception as e:  # noqa: BLE001
        log.exception("Unexpected error: %s", e)
        return JSONResponse(..., status_code=500)

    log.info(
        "User made a move. Match ID: %s, User ID: %s",
        move_response.match_id,
        move_response.user_id,
    )
    return JSONResponse(
        content={"data": move_response.model_dump()},
        status_code=HTTPStatus.OK,
    )
