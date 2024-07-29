import pytest
from httpx import AsyncClient

from tests.fakes import (
    TEST_ROUTER_GET_DYNAMICS,
    TEST_ROUTER_GET_LAST_TRADING_DATES_BY_QUERY,
)
from tests.unit.conftest import add_results, clean_data


class TestSTRRouters:
    @pytest.mark.parametrize(
        "value, expected_result, expectation",
        TEST_ROUTER_GET_LAST_TRADING_DATES_BY_QUERY,
    )
    async def test_get_last_trading_dates_router(
        self,
        value,
        expected_result,
        expectation,
        async_client: AsyncClient,
        clean_data,
        add_results,
    ):
        await clean_data()
        await add_results()
        response = await async_client.get(
            "/api/v1/str/last_trading_dates", params={"value": value}
        )

        with expectation:
            assert response.status_code == 200
            assert len(response.json()) == expected_result

    @pytest.mark.parametrize(
        "start_date, end_date, expected_result, expectation", TEST_ROUTER_GET_DYNAMICS
    )
    async def test_get_dynamics_router(
        self,
        start_date,
        end_date,
        expected_result,
        expectation,
        async_client: AsyncClient,
        clean_data,
        add_results,
        fastapi_cache,
    ):
        await clean_data()
        await add_results()
        date_format = "%Y-%m-%d"
        response = await async_client.get(
            "/api/v1/str/dynamics",
            params={"start_date": start_date, "end_date": end_date},
        )
        with expectation:
            assert response.status_code == 200
            assert len(response.json()) == len(expected_result)
            assert response.json()[0]["payload"]["date"] == expected_result[
                0
            ].date.strftime(date_format)
            assert response.json()[-1]["payload"]["date"] == expected_result[
                -1
            ].date.strftime(date_format)

    async def test_get_trading_results_router(
        self, async_client: AsyncClient, clean_data, add_results, fastapi_cache
    ):
        await clean_data()
        await add_results()

        response = await async_client.get("/api/v1/str/trading_results")
        assert response.status_code == 200
        assert len(response.json()) == 4
