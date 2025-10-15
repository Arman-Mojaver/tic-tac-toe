from database import session
from database.models import Match, User
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
from src.schemas import CreateMoveData, MoveResponse


def create_move_view(create_move_data: CreateMoveData) -> MoveResponse:
    user = session.query(User).filter_by(id=create_move_data.user_id).one_or_none()
    if not user:
        err = f"User not found. ID: {create_move_data.user_id}"
        raise UserNotFoundError(err)

    match = session.query(Match).filter_by(id=create_move_data.match_id).one_or_none()
    if not match:
        err = f"Match not found. ID: {create_move_data.match_id}"
        raise MatchNotFoundError(err)

    if create_move_data.user_id not in match.user_ids():
        err = f"User does not belong to match. User ID: {user.id}, Match ID: {match.id}"
        raise MismatchError(err)

    if match.winner_id:
        err = f"The game has already finished. The winner is: {match.winner_id}"
        raise GameFinishedError(err)

    if len(match.moves) == GameEngine.MAX_MOVE_COUNT and not match.winner_id:
        err = "The game has already finished without a winner. You can not make a move"
        raise GameFinishedError(err)

    if create_move_data.coordinates() in MoveList(match.moves).coordinates():
        err = (
            f"Square already occupied. coordinate_x: {create_move_data.coordinate_x}, "
            f"coordinate_y: {create_move_data.coordinate_y}"
        )
        raise OccupiedSquareError(err)

    game_engine = GameEngine(match=match, moves=match.moves)

    if game_engine.user_turn() != create_move_data.user_id:
        err = f"Invalid turn. It is not the turn of user_id: {create_move_data.user_id}"
        raise InvalidTurnError(err)

    move = game_engine.create_move(
        user_id=create_move_data.user_id,
        coordinate_x=create_move_data.coordinate_x,
        coordinate_y=create_move_data.coordinate_y,
    )

    session.commit()

    return MoveResponse(
        id=move.id,
        match_id=match.id,
        user_id=create_move_data.user_id,
        coordinate_x=create_move_data.coordinate_x,
        coordinate_y=create_move_data.coordinate_y,
        winner_id=match.winner_id,
    )
