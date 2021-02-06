import json
import os
import modules.PatientDataHandler as pdhandler
import modules.FinancialDataHandler as fdhandler
import modules.RSSHandler as rss

PATIENTS_CSVFILE = "440001oitacovid19patients.csv"
DATA_SUMMARY_CSVFILE = "440001oitacovid19datasummary.csv"
EXPORT_JSON_DIR = "/../../json/"

# 総病床数
TOTAL_SICKBEDS = 365

RSS_URL = "http://www.pref.oita.jp/rss/10/site-1000786.xml"


def main():
    csvfile_dir = "/../../csv/"
    patients_csvfile = os.path.dirname(
        __file__) + csvfile_dir + PATIENTS_CSVFILE
    data_summary_csvfile = os.path.dirname(
        __file__) + csvfile_dir + DATA_SUMMARY_CSVFILE
    export_json_dir = os.path.dirname(__file__) + EXPORT_JSON_DIR

    pdh = pdhandler.PatientDataHandler(
        patients_csvfile=patients_csvfile,
        data_summary_csvfile=data_summary_csvfile,
        total_sickbeds=TOTAL_SICKBEDS,
    )
    data_json = pdh.generate_data()

    with open(export_json_dir + "data.json", 'w') as f:
        json.dump(data_json, f, indent=2, ensure_ascii=False)

    loan_amount_data_csv = os.path.dirname(__file__)

    fdh = fdhandler.FinancialDataHandler(
        # TODO: あとで変数にする
        loan_amount_data_csv=os.path.dirname(
            __file__) + csvfile_dir + "440001oitacovid19finamount.csv",
        loan_counts_data_csv=os.path.dirname(
            __file__) + csvfile_dir + "440001oitacovid19finnumber.csv",
        industry_master_data_csv=os.path.dirname(
            __file__) + csvfile_dir + "440001oitacovid19fintype.csv",
        subsidy_data_csv=os.path.dirname(
            __file__) + csvfile_dir + "440001oitaemploymentsubsidy.csv"
    )
    financial_json = fdh.generate_data()

    with open(export_json_dir + "financial.json", 'w') as f:
        json.dump(financial_json, f, indent=2, ensure_ascii=False)

    rss_handler = rss.RSSHandler()
    news_json = rss_handler.generate_news(RSS_URL)

    with open(export_json_dir + "news.json", 'w') as f:
        json.dump(news_json, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
