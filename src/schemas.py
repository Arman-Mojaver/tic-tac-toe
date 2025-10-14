from pydantic import BaseModel, PositiveInt


class MatchUsers(BaseModel):
    user_x_id: PositiveInt
    user_o_id: PositiveInt
