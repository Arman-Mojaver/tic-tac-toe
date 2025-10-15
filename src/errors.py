class UserNotFoundError(Exception):
    pass


class SameUserError(Exception):
    pass


class MatchNotFoundError(Exception):
    pass


class MismatchError(Exception):
    pass


class GameFinishedError(Exception):
    pass


class OccupiedSquareError(Exception):
    pass


class InvalidTurnError(Exception):
    pass
