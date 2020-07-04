from data.domain.utils import read_csv


class FinancialApplicationService(object):
    @classmethod
    def dump_json(cls):
        fin_type = read_csv(
            "http://data.bodik.jp/dataset/a099a7d0-8393-4982-89c3-bee49ddfcecd/resource/3be72fdc-d8e7-4042-bbcd-e05e8dc6bae2/download/440001oitacovid19fintype.csv"
        )
        fin_series = read_csv(
            "http://data.bodik.jp/dataset/a099a7d0-8393-4982-89c3-bee49ddfcecd/resource/a56764ef-baba-4972-8877-e773c24d27ca/download/440001oitacovid19finnumber.csv"
        )
        fin_amount = read_csv(
            "http://data.bodik.jp/dataset/a099a7d0-8393-4982-89c3-bee49ddfcecd/resource/9c609301-4800-4f06-a400-62ba5eb489ba/download/440001oitacovid19finamount.csv"
        )
        raise NotImplementedError