import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from fastapi_filter import FilterDepends

from services.str_service import SpimexTradingResultsService
from src.filters.src_filter import STRFilter
from src.schemas.wrapper import SpimexTradingResultsWrapper
from src.utils.unit_of_work import UnitOfWork

router = APIRouter(prefix="/str")


async def get_last_days_list(value: int, uow: UnitOfWork):
    if value <= 0:
        return False
    date_list = await SpimexTradingResultsService.get_last_trading_dates_by_query(uow)
    date_list.sort(reverse=True)
    today = datetime.date.today()
    last_day = max(date_list)
    delta = datetime.timedelta(days=value)
    if today - last_day < delta:
        return date_list[:value]


@router.get("/last_trading_dates")
@cache(expire=3600 * 24)
async def get_last_trading_dates(value: int, uow: UnitOfWork = Depends(UnitOfWork)):
    date_list = await get_last_days_list(value, uow)
    if not date_list:
        return HTTPException(
            status_code=404, detail="Введите корректное значение value (больше 0)"
        )
    return date_list


@router.get("/dynamics")
@cache(expire=3600 * 24)
async def get_dynamics(
    start_date: datetime.date,
    end_date: datetime.date,
    str_filter: STRFilter = FilterDepends(STRFilter),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await SpimexTradingResultsService.get_dynamics_by_query(
        start_date, end_date, uow, str_filter
    )
    if not result:
        return HTTPException(
            status_code=404, detail="Проверьте введение корректных данных!"
        )
    return [
        SpimexTradingResultsWrapper(payload=res.to_pydantic_schema()) for res in result
    ]


@router.get("/trading_results")
@cache(expire=3600 * 24)
async def get_trading_results(
    str_filter: STRFilter = FilterDepends(STRFilter),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await SpimexTradingResultsService.get_trading_results_by_query(
        uow, str_filter
    )
    if not result:
        return HTTPException(
            status_code=404, detail="Проверьте введение корректных данных!"
        )
    return [
        SpimexTradingResultsWrapper(payload=res.to_pydantic_schema()) for res in result
    ]
