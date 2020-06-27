from abc import ABCMeta
from abc import abstractmethod
import requests
from requests.exceptions import RequestException
import io
import json
import csv


class Reader(metaclass=ABCMeta):
    @classmethod
    def fetch(cls, urls):
        """
        指定された各種ファイルをインメモリでロードする
        """
        for url in urls:
            try:
                resp = requests.get(url)
            except RequestException:
                pass

            if resp.status_code > 300:
                raise Exception(f"status code is {resp.status_code}")
            # see. https://docs.python.org/ja/3.7/library/codecs.html?highlight=utf%20sig#module-encodings.utf_8_sig
            with io.StringIO(resp.content.decode('utf-8-sig')) as bs:
                json_list = [row for row in csv.DictReader(bs)]
                yield json_list

    @abstractmethod
    def read(self):
        pass


class FinancialReader(Reader):
    # TODO: urlが長すぎるので、環境変数から読むようにする
    def __init__(self):
        base_url = "http://data.bodik.jp/dataset/a099a7d0-8393-4982-89c3-bee49ddfcecd/resource/"
        fin_number = "a56764ef-baba-4972-8877-e773c24d27ca/download/440001oitacovid19finnumber.csv"
        fin_amount = "9c609301-4800-4f06-a400-62ba5eb489ba/download/440001oitacovid19finamount.csv"
        fin_type = (
            "3be72fdc-d8e7-4042-bbcd-e05e8dc6bae2/download/440001oitacovid19fintype.csv"
        )
        self.urls = (base_url + suffix for suffix in (fin_number, fin_amount, fin_type))

    def _fetch(self):
        super().fetch(self.urls)

    def read(self):
        """
        必要な各種ファイルを読み込んだ結果をリストで返します
        Returns:
            list 
        """
        return [json_dict for json_dict in self._fetch()]


class PatientReader(Reader):
    def __init__(self):
        base_url = "http://data.bodik.jp/dataset/f632f467-716c-46aa-8838-0d535f98b291/resource/"
        patients = "3714d264-70f3-4518-a57a-8391e0851d7d/download/440001oitacovid19patients.csv"
        time_series = "96440e66-3061-43d6-adf3-ef1f24211d3a/download/440001oitacovid19datasummary.csv"
        self.urls = [base_url + suffix for suffix in (patients, time_series)]

    def _fetch(self):
        super().fetch(self.urls)

    def read(self):
        return [json_dict for json_dict in self._fetch()]
