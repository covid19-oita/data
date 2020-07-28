#!/bin/python

import json
import csv
import os
import datetime
import collections
from copy import deepcopy

from chardet.universaldetector import UniversalDetector

class DataHandler():
    def __init__(self):
        datetime_now = datetime.datetime.now()
        self.datetime_now_year_str = datetime_now.strftime("%Y")
        self.datetime_now_str = datetime_now.strftime("%Y/%m/%d %H:%M")

        self.start_date = None
        self.end_date = datetime_now if datetime_now.hour >= 22 else \
            datetime_now - datetime.timedelta(days=1)
    
    def check_encoding(self, file_path):
        detector = UniversalDetector()
        with open(file_path, mode='rb') as f:
            for binary in f:
                detector.feed(binary)
                if detector.done:
                    break
        detector.close()
        return detector.result['encoding']

    def load_json_from_csv(self, csvfile):
        json_list = []
        encoding = self.check_encoding(csvfile)
        with open(csvfile, 'r', encoding=encoding) as f:
            for row in csv.DictReader(f):
                json_list.append(row)
        return json.loads(json.dumps(json_list))

    def summarize_data_by_key(self, data, key):
        counter = [d[key] for d in data]
        summary = {}
        for val, total in collections.Counter(counter).items():
            summary[val] = total

        return summary

    def fill_in_zero_value_at_non_exists_date(self, summary_by_date):
        start_date = list(summary_by_date.keys())[0]
        null_date = dict.fromkeys(
            self.daterange(
                start_date, self.end_date), 0)

        return self.deepmerge(null_date, summary_by_date)

    def deepmerge(self, src, update):
        result = deepcopy(src)
        for k, v in update.items():
            if k in result and isinstance(result[k], dict):
                result[k] = self.deepmerge(result[k], v)
            else:
                result[k] = deepcopy(v)
        return result

    def filter_by_key(self, data, key):
        return list(filter(
            lambda x: len(x[key]) != 0,
            data
        ))

    def daterange(self, start_date, end_date):
        for n in range((end_date - start_date).days + 1):
            yield start_date + datetime.timedelta(n)
