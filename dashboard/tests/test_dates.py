import pytz
from datetime import datetime

from ..dates import calculate_next_nag, businesstimedelta


def test_calculate_next_nag_works_when_never_nagged():
    created_at = datetime(2017, 6, 19, 14, tzinfo=pytz.utc)
    next_nag_at = calculate_next_nag(created_at)
    assert businesstimedelta(created_at, next_nag_at).days == 45


def test_calculate_next_nag_works_when_nagged_once():
    created_at = datetime(2017, 6, 19, 14, tzinfo=pytz.utc)
    last_nagged_at = calculate_next_nag(created_at)
    next_nag_at = calculate_next_nag(created_at, last_nagged_at)
    assert businesstimedelta(created_at, next_nag_at).days == 68


def test_calculate_next_nag_works_when_nagged_a_ton():
    created_at = datetime(2017, 6, 19, 14, tzinfo=pytz.utc)
    last_nagged_at = None
    nag_days = []
    for _ in range(10):
        last_nagged_at = calculate_next_nag(created_at, last_nagged_at)
        nag_days.append(businesstimedelta(created_at, last_nagged_at).days)
    assert nag_days == [45, 68, 79, 85, 87, 88, 89, 90, 91, 92]


def create_dates_business_days_apart(days):
    assert days < 5  # This algorithm only supports a few days difference.

    year = 2017
    month = 6
    day = 19  # A monday
    hour = 14  # In the middle of the day UTC, during business hours EST

    a = datetime(year, month, day, hour, tzinfo=pytz.utc)
    b = datetime(year, month, day + days, hour, tzinfo=pytz.utc)

    return (a, b)


def test_businesstimedelta_works():
    for i in range(1, 5):
        a, b = create_dates_business_days_apart(i)
        assert businesstimedelta(a, b).days == i

    a = datetime(2017, 6, 19, 14, tzinfo=pytz.utc)

    # This is next monday (spanning the weekend).
    b = datetime(2017, 6, 26, 14, tzinfo=pytz.utc)

    assert businesstimedelta(a, b).days == 5
