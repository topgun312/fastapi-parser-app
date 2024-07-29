from typing import Sequence

import pytest

from src.models import SpimexTradingResultsModel
from utils.unit_of_work import UnitOfWork


class TestUnitOfWork:
    async def test_uow_commit(self, clean_data, results, get_results):
        await clean_data()
        uow = UnitOfWork()
        async with uow:
            for res_schema in results:
                await uow.spimex_trading_result.add_one(**res_schema.model_dump())

        res_in_db: Sequence[SpimexTradingResultsModel] = await get_results()
        assert len(res_in_db) == 4

    async def test_uow_rollback(self, clean_data, results, get_results):
        await clean_data()
        with pytest.raises(Exception):
            uow = UnitOfWork()
            async with uow:
                for res_schema in results:
                    await uow.spimex_trading_result.add_one(**res_schema.model_dump())
                raise Exception

        res_in_db: Sequence[SpimexTradingResultsModel] = await get_results()
        assert len(res_in_db) == 0
