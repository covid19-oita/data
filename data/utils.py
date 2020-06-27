from datetime import timedelta
from dateutil.relativedelta import relativedelta, SU
from dateutil.rrule import rrule, DAILY


def date_range(start_date, end_date):
    rule = rrule(freq=DAILY, dtstart=start_date, until=end_date)
    for date in list(rule):
        yield date
