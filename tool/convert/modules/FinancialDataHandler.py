import datetime
from typing import Dict

import modules.DataHandler as handler


class FinancialDataHandler(handler.DataHandler):
    def __init__(self,
                 loan_amount_data_csv: str = None,
                 loan_counts_data_csv: str = None,
                 industry_master_data_csv: str = None,
                 subsidy_data_csv: str = None) -> None:
        super().__init__()

        self.loan_amount_data = self.__import_loan_amount_data(
            loan_amount_data_csv)
        self.loan_counts_data = self.__import_loan_counts_data(
            loan_counts_data_csv)
        self.industry_master_data = self.__import_industry_master_data(
            industry_master_data_csv)
        self.subsidy_data = self.__import_subsidy_data(subsidy_data_csv)

    def generate_data(self) -> Dict:
        self.data = {
            "subsidy_summary": self.generate_subsidy_summary(),
            "subsidy": self.generate_subsidy(),
            "loan_achivements": self.generate_loan_achivements(),
            "loan_achivements_by_industry": self.generate_loan_achivements_by_industry()
        }

        return self.data

    def generate_subsidy_summary(self) -> Dict:
        subsidy_summary = {
            "data": [],
            "date": self.datetime_now_str
        }

        for d in self.subsidy_data:
            s = {
                "日付": d["基準日"].strftime("%Y-%m-%d"),
                "申請書提出件数": d["申請書提出件数"],
                "支給決定件数": d["支給決定件数"]
            }
            subsidy_summary["data"].append(s)

        return subsidy_summary

    def generate_subsidy(self) -> Dict:
        count_of_consulation_with_pref = list(map(
            lambda x: x["相談件数（県）"],
            self.subsidy_data,
        ))

        count_of_consulation_with_gov = list(map(
            lambda x: x["相談件数（国）"],
            self.subsidy_data,
        ))

        dates = list(map(
            lambda x: x["基準日"].strftime("%m/%d"),
            self.subsidy_data,
        ))

        subsidy = {
            "date": self.datetime_now_str,
            "data": {
                "労働局 (097-535-2100) への相談件数": count_of_consulation_with_gov,
                "大分県 (0120-575-626) への相談件数": count_of_consulation_with_pref,
            },
            "labels": dates
        }

        return subsidy

    def generate_loan_achivements(self):
        loan_achivements_with_gov = list(map(
            lambda x: x["新型コロナ資金"] // 10000,
            self.loan_amount_data
        ))

        loan_achivements_with_pref = list(map(
            lambda x: x["がんばろう資金"] // 10000,
            self.loan_amount_data
        ))

        dates = list(map(
            lambda x: x["基準日"].strftime("%m/%d"),
            self.loan_amount_data
        ))

        loan_achivements = {
            "date": self.datetime_now_str,
            "data": {
                "新型コロナウイルス感染症緊急対策特別資金": loan_achivements_with_gov,
                "がんばろう！おおいた資金繰り応援資金": loan_achivements_with_pref
            },
            "labels": dates
        }

        return loan_achivements

    def generate_loan_achivements_by_industry(self):
        count_by_industry = {d: 0 for d in self.industry_master_data.values()}
        for d in self.loan_counts_data:
            count_by_industry[self.industry_master_data[d["業種コード"]]] += d["件数"]

        loan_achivements_by_industry = {
            "date": self.datetime_now_str,
            "data": count_by_industry
        }

        return loan_achivements_by_industry

    def __import_loan_amount_data(self, csvfile: str) -> Dict:
        loan_amount_data = self.filter_by_key(
            self.load_json_from_csv(csvfile), "基準日")

        for d in loan_amount_data:
            d["基準日"] = datetime.datetime.strptime(d["基準日"], "%Y/%m/%d")
            d["がんばろう資金"] = int(d["がんばろう資金"] or 0)
            d["新型コロナ資金"] = int(d["新型コロナ資金"] or 0)

        return loan_amount_data

    def __import_loan_counts_data(self, csvfile: str) -> Dict:
        loan_counts_data = self.filter_by_key(
            self.load_json_from_csv(csvfile), "基準日")

        for d in loan_counts_data:
            d["基準日"] = datetime.datetime.strptime(d["基準日"], "%Y/%m/%d")
            d["業種コード"] = int(d["業種コード"] or 0)
            d["件数"] = int(d["件数"] or 0)

        return loan_counts_data

    def __import_industry_master_data(self, csvfile: str) -> Dict:
        master = self.filter_by_key(
            self.load_json_from_csv(csvfile),
            "業種コード"
        )

        industry_master_data = {}
        for d in master:
            industry_master_data[int(d["業種コード"])] = d["業種名"]

        return industry_master_data

    def __import_subsidy_data(self, csvfile: str) -> Dict:
        subsidy_data = self.filter_by_key(
            self.load_json_from_csv(csvfile), "基準日")

        for d in subsidy_data:
            d["基準日"] = datetime.datetime.strptime(d["基準日"], "%Y/%m/%d")
            d["相談件数（県）"] = int(d["相談件数（県）"] or 0)
            d["相談件数（国）"] = int(d["相談件数（国）"] or 0)
            d["申請書提出件数"] = int(d["申請書提出件数"] or 0)
            d["支給決定件数"] = int(d["支給決定件数"] or 0)

        return subsidy_data


def main():
    dh = FinancialDataHandler(
        loan_amount_data_csv="/home/varu3/go/src/github.com/covid19-oita/data/csv/440001oitacovid19finamount.csv",
        loan_counts_data_csv="/home/varu3/go/src/github.com/covid19-oita/data/csv/440001oitacovid19finnumber.csv",
        industry_master_data_csv="/home/varu3/go/src/github.com/covid19-oita/data/csv/440001oitacovid19fintype.csv",
        subsidy_data_csv="/home/varu3/go/src/github.com/covid19-oita/data/csv/440001oitaemploymentsubsidy.csv"
    )
    dh.generate_data()


if __name__ == "__main__":
    main()
