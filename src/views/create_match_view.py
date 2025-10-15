from database import session
from database.models import Match, User
from src.errors import SameUserError, UserNotFoundError
from src.schemas import CreateMatchData, MatchResponse


def create_match_view(create_match_data: CreateMatchData) -> MatchResponse:
    user_x = session.query(User).filter_by(id=create_match_data.user_x_id).one_or_none()
    if not user_x:
        err = f"User not found. ID {create_match_data.user_x_id}"
        raise UserNotFoundError(err)

    user_o = session.query(User).filter_by(id=create_match_data.user_o_id).one_or_none()
    if not user_o:
        err = f"User not found. ID {create_match_data.user_o_id}"
        raise UserNotFoundError(err)

    if user_x.id == user_o.id:
        err = f"User ids can not be the same. ID: {user_x.id}"
        raise SameUserError(err)

    match = Match(user_x_id=user_x.id, user_o_id=user_o.id)
    session.add(match)
    session.commit()
    session.refresh(match)

    return MatchResponse(match_id=match.id)
