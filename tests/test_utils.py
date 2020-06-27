import pytest
from data.utils import date_range
from datetime import datetime
from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta, SU
from dateutil.rrule import rrule, DAILY


def test_date_range():
    start_date = datetime(2020, 1, 1).date()
    end_date = datetime(2020, 1, 3).date()
    wants = [datetime(2020, 1, 1), datetime(2020, 1, 2), datetime(2020, 1, 3)]
    got = [d for d in date_range(start_date, end_date)]
    assert wants == got
