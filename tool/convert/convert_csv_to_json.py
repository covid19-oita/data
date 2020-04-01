#!/bin/python

import json
import csv
import os
import sys
import datetime
import collections
from copy import deepcopy

PATIENTS_DATA_CSV_FILE_NAME = "440001_oita_covid19_patients.csv"
INSPECTIONS_DATA_CSV_FILE_NAME = "440001_oita_covid19_inspections.csv"

def main():
    patients_data_csv_file = os.path.dirname(__file__) + "/../../static/data/" + PATIENTS_DATA_CSV_FILE_NAME
    inspections_data_csv_file = os.path.dirname(__file__) + "/../../static/data/" + INSPECTIONS_DATA_CSV_FILE_NAME
    export_json_file = os.path.dirname(__file__) + "/../../data/data.json"

    if os.path.exists(patients_data_csv_file) == False or os.path.exists(inspections_data_csv_file) == False:
        print("CSV data files are not found.")
        sys.exit(1)

    patients_data = import_csv_to_dict(patients_data_csv_file, encoding='utf_8_sig')
    inspections_data = import_csv_to_dict(inspections_data_csv_file, encoding='utf_8_sig')

    patients = generate_patients(patients_data)
    patients_summary = generate_patients_summary(patients_data)
    inspections_summary = generate_inspections_summary(inspections_data)

    today_date_string = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    data_json = {
        "patients": {
            "date": today_date_string,
            "data": patients,
        },
        "patients_summary": {
            "date": today_date_string,
            "data": patients_summary,
        },
        "inspections_summary": {
            "date": today_date_string,
            "data": inspections_summary,
        },
        "lastUpdate": today_date_string
    }

    with open(export_json_file, 'w') as f:
        json.dump(data_json, f, indent=2, ensure_ascii=False)


def import_csv_to_dict(csv_file, encoding='utf_8_sig'):
    json_list = []
    with open(csv_file, 'r', encoding=encoding) as f:
        for row in csv.DictReader(f): json_list.append(row)
    return json.loads(json.dumps(json_list))

def generate_patients(data):
    patients = []
    for d in data:
        p = {
            "リリース日": d["公表_年月日"] + "T08:00:00",
            "居住地": d["居住地"],
            "年代": d["年代"],
            "性別": d["性別"],
            "退院": d["退院済フラグ"],
            "date": d["公表_年月日"]
        }
        patients.append(p)

    return patients

def generate_patients_summary(data):
    counted_date = [ datetime.datetime.strptime(d["公表_年月日"], '%Y-%m-%d') for d in data ]

    start_date = sorted(counted_date)[0]
    end_date   = datetime.datetime.now()

    # 日付に対して値が0のデータを作る
    df_date = {}
    for i in daterange(start_date, end_date):
        df_date[i] = 0

    df_patients_summary = {}
    for date, total in collections.Counter(counted_date).items():
        df_patients_summary[date] = total

    df = deepmerge(df_date, df_patients_summary)

    patients_summary = []
    for date, total in df.items():
        ps = {
            "日付": date.strftime("%Y-%m-%d"),
            "小計": total,
        }
        patients_summary.append(ps)

    return patients_summary

def generate_inspections_summary(data):
    parsed_data = [ { "日付": datetime.datetime.strptime(d["日付"], "%Y-%m-%d"), "小計": int(d["検査人数"]) } for d in data ]

    counted_date = [ pd["日付"] for pd in parsed_data ]
    start_date = sorted(counted_date)[0]
    end_date   = datetime.datetime.now()

    # 日付に対して値が0のデータを作る
    df_date = {}
    for i in daterange(start_date, end_date): df_date[i] = 0

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
