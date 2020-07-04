import csv
from datetime import datetime
import io
from typing import Dict, List
from dateutil.rrule import DAILY, rrule
import requests


def read_csv(url: str) -> List[Dict[str, str]]:
    """
    URLからCSVを取得します
    """
    resp = requests.get(url)
    with io.StringIO(resp.content.decode('utf-8-sig')) as bs:
        json_list = [row for row in csv.DictReader(bs)]
    return json_list


def join_fintype():
    pass


def date_range(start_date, end_date):
    rule = rrule(freq=DAILY, dtstart=start_date, until=end_date)
    for date in list(rule):
        yield date


def format_date(date: str):
    """
    入力された日付文字列(m月d日)に現在の年情報を追加します。
    Args:
    date: str: 日付文字列(m月d日)
    Returns:
    str: 日付文字列(Y年m月d日)
    NOTE: 2021年にも対応できるように修正する必要があります。
    """
    year = datetime.now().year
    return f"{year}年{date}"
