from src.models import SpimexTradingResultsModel
from src.utils.repository import SqlAlchemyRepository


class SpimexTradingResultsRepository(SqlAlchemyRepository):
    model = SpimexTradingResultsModel
