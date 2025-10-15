from database import session
from database.models import Match, Move, User
from database.models.move import MoveList
from src.errors import (
    GameFinishedError,
    InvalidTurnError,
    MatchNotFoundError,
    MismatchError,
    OccupiedSquareError,
    UserNotFoundError,
)
from src.game_engine import GameEngine
from src.schemas import MoveData


def create_move_view(move_data: MoveData) -> Move:
    user = session.query(User).filter_by(id=move_data.user_id).one_or_none()
    if not user:
        err = f"User not found. ID: {move_data.user_id}"
        raise UserNotFoundError(err)

    match = session.query(Match).filter_by(id=move_data.match_id).one_or_none()
    if not match:
        err = f"Match not found. ID: {move_data.match_id}"
        raise MatchNotFoundError(err)

    if move_data.user_id not in match.user_ids():
        err = f"User does not belong to match. User ID: {user.id}, Match ID: {match.id}"
        raise MismatchError(err)

    if match.winner_id:
        err = f"The game has already finished. The winner is: {match.winner_id}"
        raise GameFinishedError(err)

    if len(match.moves) == GameEngine.MAX_MOVE_COUNT and not match.winner_id:
        err = "The game has already finished without a winner. You can not make a move"
        raise GameFinishedError(err)

    if move_data.coordinates() in MoveList(match.moves).coordinates():
        err = (
            f"Square already occupied. coordinate_x: {move_data.coordinate_x}, "
            f"coordinate_y: {move_data.coordinate_y}"
        )
        raise OccupiedSquareError(err)

    game_engine = GameEngine(match=match, moves=match.moves)

    if game_engine.user_turn() != move_data.user_id:
        err = f"Invalid turn. It is not the turn of user_id: {move_data.user_id}"
        raise InvalidTurnError(err)

    return game_engine.create_move(
        user_id=move_data.user_id,
        coordinate_x=move_data.coordinate_x,
        coordinate_y=move_data.coordinate_y,
    )
