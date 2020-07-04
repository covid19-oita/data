import csv
import io
from typing import Dict, List
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
