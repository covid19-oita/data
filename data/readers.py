from abc import ABCMeta, abstractmethod
import requests
from requests.exceptions import RequestException
import io
import json
import csv


class CSVReader(metaclass=ABCMeta):
    @abstractmethod
    def _fetch(self):
        pass

    @abstractmethod
    def read(self):
        pass


class FinancialReader(CSVReader):
    """
    大分県の金融支援情報に関するファイルを読み込みます
    """

    def __init__(self):
        base_url = "http://data.bodik.jp/dataset/a099a7d0-8393-4982-89c3-bee49ddfcecd/resource/"
        fin_number = "a56764ef-baba-4972-8877-e773c24d27ca/download/440001oitacovid19finnumber.csv"
        fin_amount = "9c609301-4800-4f06-a400-62ba5eb489ba/download/440001oitacovid19finamount.csv"
        fin_type = (
            "3be72fdc-d8e7-4042-bbcd-e05e8dc6bae2/download/440001oitacovid19fintype.csv"
        )
        self.urls = (base_url + suffix for suffix in (fin_number, fin_amount, fin_type))

    @classmethod
    def _fetch(cls, url):
        """
        指定された各種ファイルをインメモリでロードする
        """
        try:
            resp = requests.get(url)
        except RequestException:
            pass

        if resp.status_code > 300:
            raise Exception(f"status code is {resp.status_code}")
        json_list = []
        with io.StringIO(resp.content.decode('utf-8-sig')) as bs:
            json_list = [row for row in csv.DictReader(bs)]
            return json_list

    def read(self):
        """
        必要な各種ファイルを読み込んだ結果をリストで返します
        Returns:
            list 
        """
        return [self._fetch(url) for url in self.urls]

