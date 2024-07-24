import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.models import BaseModel
from src.schemas.str_schema import SpimexTradingResultsSchema


class SpimexTradingResultsModel(BaseModel):
    """
    Модель результатов трейдинга
    """

    __tablename__ = "spimex_trading_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str]
    exchange_product_name: Mapped[str]
    oil_id: Mapped[str]
    delivery_basis_id: Mapped[str]
    delivery_basis_name: Mapped[str]
    delivery_type_id: Mapped[str]
    volume: Mapped[str] = mapped_column(default="-")
    total: Mapped[str] = mapped_column(default="-")
    count: Mapped[str] = mapped_column(default="-")
    date: Mapped[datetime.date]
    created_on: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_on: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
    )

    def to_pydantic_schema(self) -> SpimexTradingResultsSchema:
        return SpimexTradingResultsSchema(
            id=self.id,
            exchange_product_id=self.exchange_product_id,
            exchange_product_name=self.exchange_product_name,
            oil_id=self.oil_id,
            delivery_basis_id=self.delivery_basis_id,
            delivery_basis_name=self.delivery_basis_name,
            delivery_type_id=self.delivery_type_id,
            volume=self.volume,
            total=self.total,
            count=self.count,
            date=self.date,
        )
