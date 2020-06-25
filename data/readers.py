from abc import ABCMeta, abstractmethod
import requests

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
        fin_type = "3be72fdc-d8e7-4042-bbcd-e05e8dc6bae2/download/440001oitacovid19fintype.csv"
        self.fin_number_url = base_url + fin_number
        self.fin_amount_url = base_url + fin_amount
        self.fin_type_url = base_url + fin_type
    
    def _fetch(self):
        """
        指定された各種ファイルをインメモリでロードする
        """
        requests



        


    def read(self):
        




"""
def read(reader):
    pass

fin_reader = FinanCialReader()
read(fin_reader)
"""
