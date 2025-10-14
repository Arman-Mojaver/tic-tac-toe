from fastapi import FastAPI
from fastapi.responses import JSONResponse

from database import session
from database.models import Match, User
from src.schemas import MatchUsers

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
