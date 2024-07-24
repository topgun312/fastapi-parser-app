from pydantic import BaseModel

from src.schemas.str_schema import SpimexTradingResultsSchema


class BaseWrapper(BaseModel):
    status: int = 200
    error: bool = False


class SpimexTradingResultsWrapper(BaseWrapper):
    status: int = 201
    payload: SpimexTradingResultsSchema
