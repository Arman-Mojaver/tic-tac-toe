from database import session
from database.models import Match
from src.errors import MatchNotFoundError
from src.game_engine import GameEngine
from src.schemas import StatusResponse


def get_status_view(match_id: int) -> StatusResponse:
    match = session.query(Match).filter_by(id=match_id).one_or_none()
    if not match:
        err = f"Match ID not found: {match_id}"
        raise MatchNotFoundError(err)

    game_engine = GameEngine(match=match, moves=match.moves)
    return game_engine.status()
