from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from models import SpimexTradingResultsModel


class STRFilter(Filter):
    """
    Класс для фильтрации запросов по oil_id, delivery_type_id, delivery_basis_id
    """

    oil_id: Optional[str] = None
    delivery_type_id: Optional[str] = None
    delivery_basis_id: Optional[str] = None

    class Constants(Filter.Constants):
        model = SpimexTradingResultsModel
