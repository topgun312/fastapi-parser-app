import datetime
from contextlib import nullcontext as does_not_raise
from copy import deepcopy

import pytest

from tests.fakes.str_fakes import FAKE_RESULTS


TEST_BASE_SERVICE_GET_LAST_TRADING_DATES_BY_QUERY_PARAMS = [
    (2, 2, does_not_raise()),
    (3, 3, does_not_raise()),
    (-2, 2, pytest.raises(Exception)),
    ("string", 2, pytest.raises(Exception)),
]


TEST_BASE_SERVICE_GET_DYNAMICS = [
    (
        datetime.date(2024, 7, 23),
        datetime.date(2024, 7, 24),
        [FAKE_RESULTS[0], FAKE_RESULTS[1]],
        does_not_raise(),
    ),
    (
        datetime.date(2024, 7, 23),
        datetime.date(2024, 7, 25),
        [FAKE_RESULTS[0], FAKE_RESULTS[1], FAKE_RESULTS[2]],
        does_not_raise(),
    ),
    (
        "23-07-2024",
        "24-07-2024",
        [FAKE_RESULTS[0], FAKE_RESULTS[1]],
        pytest.raises(Exception),
    ),
]


TEST_SQLALCHEMY_REPOSITORY_GET_LAST_TRADING_DATES_BY_QUERY_PARAMS = [
    datetime.date(2024, 7, 23),
    datetime.date(2024, 7, 24),
    datetime.date(2024, 7, 25),
    datetime.date(2024, 7, 26),
]
TEST_SQLALCHEMY_REPOSITORY_GET_DYNAMICS = deepcopy(TEST_BASE_SERVICE_GET_DYNAMICS)

TEST_ROUTER_GET_DYNAMICS = deepcopy(TEST_BASE_SERVICE_GET_DYNAMICS)
TEST_ROUTER_GET_LAST_TRADING_DATES_BY_QUERY = deepcopy(
    TEST_BASE_SERVICE_GET_LAST_TRADING_DATES_BY_QUERY_PARAMS
)
