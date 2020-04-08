#!/bin/python

import json
import csv
import os
import sys
import datetime
import collections
from copy import deepcopy

PATIENTS_DATA_CSV_FILE_NAME = "440001oitacovid19patients.csv"
DATA_SUMMARY_CSV_FILE_NAME = "440001oitacovid19datasummary.csv"

# 総病床数
TOTAL_SICK_BEDS = 118


def main():
    patients_data_csv_file = os.path.dirname(
        __file__) + "/../../csv/" + PATIENTS_DATA_CSV_FILE_NAME
    data_summary_csv_file = os.path.dirname(
        __file__) + "/../../csv/" + DATA_SUMMARY_CSV_FILE_NAME
    export_json_file = os.path.dirname(__file__) + "/../../json/data.json"

    if not os.path.exists(patients_data_csv_file) or not os.path.exists(
            data_summary_csv_file):
        print("CSV data files are not found.")
        sys.exit(1)

    patients_data = import_csv_to_dict(
        patients_data_csv_file, encoding='utf_8_sig')
    data_summary = import_csv_to_dict(
        data_summary_csv_file, encoding='utf_8_sig')

    datetime_now_str = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")

    patients = generate_patients(patients_data)
    patients_summary_by_date = generate_patients_summary_by_date(patients_data)
    patients_summary_by_age = generate_patients_summary_by_age(patients_data)

    inspections_summary = generate_inspections_summary(data_summary)
    sickbeds_summary = generate_sickbeds_summary(data_summary)
    main_summary = generate_main_summary(data_summary)
    main_summary["date"] = datetime_now_str
    querents = generate_querents(data_summary)

    data_json = {
        "patients": {
            "date": datetime_now_str,
            "data": patients,
        },
        "patients_summary": {
            "date": datetime_now_str,
            "data": patients_summary_by_date,
        },
        "inspections_summary": {
            "date": datetime_now_str,
            "data": inspections_summary,
        },
        "age": {
            "date": datetime_now_str,
            "data": patients_summary_by_age,
        },
        "sickbeds_summary": {
            "date": datetime_now_str,
            "data": sickbeds_summary,
        },
        "main_summary": main_summary,
        "querents": {
            "date": datetime_now_str,
            "data": querents
        },
        "lastUpdate": datetime_now_str
    }

    with open(export_json_file, 'w') as f:
        json.dump(data_json, f, indent=2, ensure_ascii=False)


def import_csv_to_dict(csv_file, encoding='utf_8_sig'):
    json_list = []
    with open(csv_file, 'r', encoding=encoding) as f:
        for row in csv.DictReader(f):
            json_list.append(row)
    return json.loads(json.dumps(json_list))


def generate_patients(data):
    patients = []
    for d in data:
        datetime_type_datetime = datetime.datetime.strptime(
            d["公表_年月日"], '%Y/%m/%d')
        datetime_str = datetime_type_datetime.strftime("%Y-%m-%d")
        p = {
            "リリース日": datetime_str + "T08:00:00",
            "居住地": d["居住地"],
            "年代": d["年代"],
            "性別": d["性別"],
            "退院": d["退院済フラグ"],
            "date": datetime_str
        }
        patients.append(p)

    return patients


def generate_patients_summary_by_date(data):
    summary_by_date = summarize_data(data, "公表_年月日")

    df_patients_summary = {}
    for k, v in summary_by_date.items():
        df_patients_summary[datetime.datetime.strptime(k, '%Y/%m/%d')] = v

    # 日付に対して値が0のデータを作る
    start_date = sorted(list(df_patients_summary.keys()))[0]

    datetime_now = datetime.datetime.now()
    end_date = datetime_now if datetime_now.hour >= 22 else \
        datetime_now - datetime.timedelta(days=1)

    df_date = {}
    for i in daterange(start_date, end_date):
        df_date[i] = 0

    df = deepmerge(df_date, df_patients_summary)

    patients_summary_by_date = []
    for date, total in df.items():
        ps = {
            "日付": date.strftime("%Y-%m-%d"),
            "小計": total,
        }
        patients_summary_by_date.append(ps)

    return patients_summary_by_date


def generate_inspections_summary(data):
    # 日付に年が入っていないのでここで補足する。
    parsed_data = [{"日付": datetime.datetime.strptime(d["日付"], "%m月%d日").replace(
        year=2020), "小計": int(d["検査実施件数"])} for d in data if len(d["検査実施件数"]) != 0]

    counted_date = [pd["日付"] for pd in parsed_data]
    start_date = sorted(counted_date)[0]

    datetime_now = datetime.datetime.now()
    end_date = datetime_now if datetime_now.hour >= 22 else \
        datetime_now - datetime.timedelta(days=1)

    # 日付に対して値が0のデータを作る
    df_date = {}
    for i in daterange(start_date, end_date):
        df_date[i] = 0

    df_inspections_summary = {}
    for pd in parsed_data:
        df_inspections_summary[pd["日付"]] = pd["小計"]

    df = deepmerge(df_date, df_inspections_summary)

    inspections_summary = []
    for date, total in df.items():
        ps = {
            "日付": date.strftime("%Y-%m-%d"),
            "小計": total,
        }
        inspections_summary.append(ps)

    return inspections_summary


def generate_patients_summary_by_age(data):
    df_patients_summary_by_age = summarize_data(data, "年代")
    df_age = {}
    for i in range(10, 110, 10):
        df_age[str(i) + "代"] = 0

    df = deepmerge(df_age, df_patients_summary_by_age)
    patients_summary_by_age = {
        "10代以下": df["10代"],
        "20代〜30代": df["20代"] + df["30代"],
        "40代〜50代": df["40代"] + df["50代"],
        "60代〜70代": df["60代"] + df["70代"],
        "80代以上": df["80代"] + df["90代"] + df["100代"],
    }

    return patients_summary_by_age


def generate_sickbeds_summary(data):
    patients, discharges, inpatients, _ = classfy_total_patients(data)
    sickbeds_summary = {
        "入院患者数": inpatients,
        "病床数": TOTAL_SICK_BEDS - inpatients,
    }
    return sickbeds_summary


def generate_main_summary(data):
    patients, discharges, inpatients, deaths = classfy_total_patients(data)
    main_summary = {
        "attr": "累計",
        "value": patients,
        "children": [
            {"attr": "入院中", "value": inpatients},
            {"attr": "死亡", "value": deaths},
            {"attr": "退院", "value": discharges},
        ]
    }
    return main_summary


def generate_querents(data):
    # 日付に年が入っていないのでここで補足する。
    parsed_data = [
        {
            "日付": datetime.datetime.strptime(
                d["日付"],
                "%m月%d日").replace(
                year=2020).strftime("%Y-%m-%d"),
            "小計": int(d["相談窓口相談件数"])
        } for d in data if len(d["相談窓口相談件数"]) != 0]

    return parsed_data


def classfy_total_patients(data):
    patients = sum([int(d["うち陽性"]) for d in data if len(d["うち陽性"]) != 0])
    discharges = sum([int(d["退院"]) for d in data if len(d["退院"]) != 0])
    inpatients = patients - discharges
    deaths = sum([int(d["死亡"]) for d in data if len(d["死亡"]) != 0])

    return patients, discharges, inpatients, deaths


def summarize_data(data, key):
    counted = [d[key] for d in data]

    summary = {}
    for val, total in collections.Counter(counted).items():
        summary[val] = total

    return summary


def deepmerge(src, update):
    result = deepcopy(src)
    for k, v in update.items():
        if k in result and isinstance(result[k], dict):
            result[k] = deepmerge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result


def daterange(start_date, end_date):
    for n in range((end_date - start_date).days + 1):
        yield start_date + datetime.timedelta(n)


if __name__ == "__main__":
    main()
