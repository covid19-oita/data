#!/bin/python

import json
import csv
import os
import datetime
import collections
from copy import deepcopy


class DataHandler():
    def __init__(self, patients_csvfile=None, data_summary_csvfile=None, total_sickbeds=None):
        datetime_now = datetime.datetime.now()
        self.datetime_now_str = datetime_now.strftime("%Y/%m/%d %H:%M")

        self.start_date = None
        self.end_date = datetime_now if datetime_now.hour >= 22 else \
            datetime_now - datetime.timedelta(days=1)

        self.patients_csvfile = patients_csvfile
        self.patients_data = self.__import_patients_data()

        self.data_summary_csvfile = data_summary_csvfile
        self.data_summary = self.__import_data_summary()

        self.total_patients = None
        self.total_discharges = None
        self.total_deaths = None
        self.current_inpatients = None
        self.total_sickbeds = total_sickbeds
        self.__classfy_data_summary()

        self.data = {
            "patients": {
                "date": self.datetime_now_str,
                "data": {}
            },
            "patients_summary": {
                "date": self.datetime_now_str,
                "data": {}
            },
            "inspections_summary": {
                "date": self.datetime_now_str,
                "data": {}
            },
            "age": {
                "date": self.datetime_now_str,
                "data": {}
            },
            "sickbeds_summary": {
                "date": self.datetime_now_str,
                "data": {}
            },
            "main_summary": {},
            "querents": {
                "date": self.datetime_now_str,
                "data": {}
            },
            "lastUpdate": self.datetime_now_str
        }

    def generate_data(self):
        self.data["patients"]["data"] = self.generate_patients()
        self.data["patients_summary"]["data"] = self.generate_patients_summary_by_date()
        self.data["age"]["data"] = self.generate_patients_summary_by_age()
        self.data["inspections_summary"]["data"] = self.generate_inspections_summary()
        self.data["sickbeds_summary"]["data"] = self.generate_sickbeds_summary()
        self.data["main_summary"] = self.generate_main_summary()
        self.data["querents"]["data"] = self.generate_querents()

        return self.data

    def generate_patients(self):
        patients = []
        for d in self.patients_data:
            p = {
                "リリース日": d["公表_年月日"].strftime("%Y-%m-%d") + "T08:00:00",
                "居住地": d["居住地"],
                "年代": d["年代"],
                "性別": d["性別"],
                "退院": d["退院済フラグ"],
                "date": d["公表_年月日"].strftime("%Y-%m-%d")
            }
            patients.append(p)

        return patients

    def generate_patients_summary_by_date(self):
        summary_by_date = self.__summarize_data(self.patients_data, "公表_年月日")
        patients_summary_by_date = self.__fill_in_zero_value_at_non_exists_date(
            summary_by_date)

        patients_summary = []
        for date, total in patients_summary_by_date.items():
            p = {
                "日付": date.strftime("%Y-%m-%d"),
                "小計": total,
            }
            patients_summary.append(p)

        return patients_summary

    def generate_patients_summary_by_age(self):
        summary_by_age = self.__summarize_data(self.patients_data, "年代")
        null_data = {"10代未満": 0, "非公開": 0}
        for i in range(10, 110, 10):
            null_data[str(i) + "代"] = 0

        d = self.__deepmerge(null_data, summary_by_age)
        patients_summary_by_age = {
            "10代以下": d["10代"] + d["10代未満"],
            "20代〜30代": d["20代"] + d["30代"],
            "40代〜50代": d["40代"] + d["50代"],
            "60代〜70代": d["60代"] + d["70代"],
            "80代以上": d["80代"] + d["90代"] + d["100代"]
        }

        return patients_summary_by_age

    def generate_inspections_summary(self):
        inspections_summary = []
        for d in self.data_summary:
            if d["検査実施件数"] is not None:
                p = {
                    "日付": d["日付"].strftime("%Y-%m-%d"),
                    "小計": d["検査実施件数"]
                }
                inspections_summary.append(p)

        return inspections_summary

    def generate_sickbeds_summary(self):
        sickbeds_summary = {
            "入院患者数": self.current_inpatients,
            "病床数": self.total_sickbeds - self.current_inpatients
        }

        return sickbeds_summary

    def generate_main_summary(self):
        main_summary = {
            "date": self.datetime_now_str,
            "attr": "累計",
            "value": self.total_patients,
            "children": [
                {"attr": "入院中", "value": self.current_inpatients},
                {"attr": "死亡", "value": self.total_deaths},
                {"attr": "退院", "value": self.total_discharges},
            ]
        }

        return main_summary

    def generate_querents(self):
        querents = []
        for d in self.data_summary:
            if d["相談窓口相談件数"] is not None:
                q = {
                    "日付": d["日付"].strftime("%Y-%m-%d"),
                    "小計": d["相談窓口相談件数"]
                }
                querents.append(q)

        return querents

    def __import_patients_data(self):
        # 公表_年月日が空の場合はfilterする
        patients_data = list(filter(
            lambda x: len(x["公表_年月日"]) != 0,
            self.__load_csvfile(self.patients_csvfile)
        ))

        for d in patients_data:
            d["公表_年月日"] = datetime.datetime.strptime(d["公表_年月日"], '%Y/%m/%d')
            # 年代が空欄の場合は"非公開"とする
            d["年代"] = "非公開" if not d["年代"] else d["年代"]

        return patients_data

    def __import_data_summary(self):
        data_summary = list(filter(
            lambda x: len(x["日付"]) != 0,
            self.__load_csvfile(self.data_summary_csvfile)
        ))

        for d in data_summary:
            d["日付"] = datetime.datetime.strptime(
                d["日付"], "%m月%d日").replace(year=2020)
            d["検査実施件数"] = int(d["検査実施件数"]) if d["検査実施件数"] else None
            d["うち陽性"] = int(d["うち陽性"] or 0)
            d["相談窓口相談件数"] = int(d["相談窓口相談件数"]) if d["相談窓口相談件数"] else None
            d["退院"] = int(d["退院"] or 0)
            d["死亡"] = int(d["死亡"] or 0)

        start_date = data_summary[-1]["日付"] + datetime.timedelta(days=1)
        for date in self.__daterange(start_date, self.end_date):
            data_summary.append({
                "日付": date,
                "検査実施件数": None,
                "うち陽性": 0,
                "相談窓口相談件数": None,
                "退院": 0,
                "死亡": 0
            })

        return data_summary

    def __load_csvfile(self, csvfile, encoding='utf_8_sig'):
        json_list = []
        with open(csvfile, 'r', encoding=encoding) as f:
            for row in csv.DictReader(f):
                json_list.append(row)

        return json.loads(json.dumps(json_list))

    def __summarize_data(self, data, key):
        counter = [d[key] for d in data]
        summary = {}
        for val, total in collections.Counter(counter).items():
            summary[val] = total

        return summary

    def __fill_in_zero_value_at_non_exists_date(self, summary_by_date):
        start_date = list(summary_by_date.keys())[0]
        null_date = dict.fromkeys(
            self.__daterange(
                start_date, self.end_date), 0)

        return self.__deepmerge(null_date, summary_by_date)

    def __classfy_data_summary(self):
        self.total_patients = sum([d["うち陽性"] for d in self.data_summary])
        self.total_discharges = sum([d["退院"] for d in self.data_summary])
        self.total_deaths = sum([d["死亡"] for d in self.data_summary])

        self.current_inpatients = self.total_patients - \
            self.total_discharges - self.total_deaths

    def __deepmerge(self, src, update):
        result = deepcopy(src)
        for k, v in update.items():
            if k in result and isinstance(result[k], dict):
                result[k] = self.__deepmerge(result[k], v)
            else:
                result[k] = deepcopy(v)
        return result

    def __daterange(self, start_date, end_date):
        for n in range((end_date - start_date).days + 1):
            yield start_date + datetime.timedelta(n)
