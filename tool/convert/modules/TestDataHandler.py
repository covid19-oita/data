#!/bin/python

import datetime
import os
import unittest
import json
import DataHandler as handler

PATIENTS_CSVFILE = "test_440001oitacovid19patients.csv"
DATA_SUMMARY_CSVFILE = "test_440001oitacovid19datasummary.csv"


class ConvertTest(unittest.TestCase):
    maxDiff = None
    datetime_now_str = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    patients_csvfile = os.path.dirname(
        __file__) + "/test/csv/" + PATIENTS_CSVFILE
    data_summary_csvfile = os.path.dirname(
        __file__) + "/test/csv/" + DATA_SUMMARY_CSVFILE

    def test_generate_patients(self):
        expect_json = '''
[{
  "リリース日": "2020-03-17T08:00:00",
  "居住地": "大分市",
  "年代": "10代",
  "性別": "女性",
  "退院": "",
  "date": "2020-03-17"
},
{
  "リリース日": "2020-03-19T08:00:00",
  "居住地": "臼杵市",
  "年代": "20代",
  "性別": "男性",
  "退院": "",
  "date": "2020-03-19"
},
{
  "リリース日": "2020-03-19T08:00:00",
  "居住地": "臼杵市",
  "年代": "30代",
  "性別": "女性",
  "退院": "",
  "date": "2020-03-19"
},
{
  "リリース日": "2020-03-20T08:00:00",
  "居住地": "大分市",
  "年代": "40代",
  "性別": "女性",
  "退院": "",
  "date": "2020-03-20"
},
{
  "リリース日": "2020-03-20T08:00:00",
  "居住地": "大分市",
  "年代": "60代",
  "性別": "女性",
  "退院": "",
  "date": "2020-03-20"
},
{
  "リリース日": "2020-03-20T08:00:00",
  "居住地": "大分市",
  "年代": "90代",
  "性別": "女性",
  "退院": "",
  "date": "2020-03-20"
}]
'''.strip()

        expect = json.loads(expect_json)
        dh = handler.DataHandler(
            patients_csvfile=self.patients_csvfile,
            data_summary_csvfile=self.data_summary_csvfile
        )
        result = dh.generate_patients()

        self.assertListEqual(result, expect)

    def test_generate_patients_summary_by_date(self):

        expect_json = '''
[{
  "日付": "2020-03-17",
  "小計": 1
},
{
  "日付": "2020-03-18",
  "小計": 0
},
{
  "日付": "2020-03-19",
  "小計": 2
},
{
  "日付": "2020-03-20",
  "小計": 3
}]
'''.strip()
        # テストデータのため2020-03-21から本日までの日付のデータを作成する
        null_data = self.__generate_null_data(datetime.datetime(2020, 3, 21))
        expect = json.loads(expect_json)
        expect.extend(null_data)

        dh = handler.DataHandler(
            patients_csvfile=self.patients_csvfile,
            data_summary_csvfile=self.data_summary_csvfile
        )
        result = dh.generate_patients_summary_by_date()

        self.assertListEqual(result, expect)

    def test_generate_inspections_summary(self):
        expect_json = '''
[{
  "日付": "2020-03-20",
  "小計": 67
},
{
  "日付": "2020-03-21",
  "小計": 111
},
{
  "日付": "2020-03-22",
  "小計": 182
},
{
  "日付": "2020-03-23",
  "小計": 205
}]
'''.strip()
        null_data = self.__generate_null_data(datetime.datetime(2020, 3, 24))
        expect = json.loads(expect_json)
        expect.extend(null_data)

        dh = handler.DataHandler(
            patients_csvfile=self.patients_csvfile,
            data_summary_csvfile=self.data_summary_csvfile,
            total_sickbeds=118
        )
        result = dh.generate_inspections_summary()

        self.assertListEqual(result, expect)

    def test_generate_patients_summary_by_age(self):
        expect_json = '''
{
  "10代以下": 1,
  "20代〜30代": 2,
  "40代〜50代": 1,
  "60代〜70代": 1,
  "80代以上": 1
}
'''.strip()

        dh = handler.DataHandler(
            patients_csvfile=self.patients_csvfile,
            data_summary_csvfile=self.data_summary_csvfile
        )
        result = dh.generate_patients_summary_by_age()
        expect = json.loads(expect_json)

        self.assertDictEqual(result, expect)

    def test_generate_sickbeds_summary(self):
        expect_json = '''
{
  "入院患者数": 18,
  "病床数": 100
}
'''.strip()

        dh = handler.DataHandler(
            patients_csvfile=self.patients_csvfile,
            data_summary_csvfile=self.data_summary_csvfile,
            total_sickbeds=118
        )
        result = dh.generate_sickbeds_summary()
        expect = json.loads(expect_json)

        self.assertDictEqual(result, expect)

    def test_generate_main_summary(self):
        expect_json = '''
{
  "attr": "累計",
  "value": 19,
  "children": [
      {
        "attr": "入院中",
        "value": 18
      },
      {
        "attr": "死亡",
        "value": 0
      },
      {
        "attr": "退院",
        "value": 1
      }
  ]
}
'''.strip()

        dh = handler.DataHandler(
            patients_csvfile=self.patients_csvfile,
            data_summary_csvfile=self.data_summary_csvfile
        )
        result = dh.generate_main_summary()
        expect = json.loads(expect_json)
        expect["date"] = self.datetime_now_str

        self.assertDictEqual(result, expect)

    def test_generate_querents(self):
        expect_json = '''
[
  {
    "日付": "2020-03-20",
    "小計": 100
  },
  {
    "日付": "2020-03-21",
    "小計": 117
  },
  {
    "日付": "2020-03-22",
    "小計": 99
  },
  {
    "日付": "2020-03-23",
    "小計": 311
  }
]
'''.strip()

        null_data = self.__generate_null_data(datetime.datetime(2020, 3, 24))
        expect = json.loads(expect_json)
        expect.extend(null_data)

        dh = handler.DataHandler(
            patients_csvfile=self.patients_csvfile,
            data_summary_csvfile=self.data_summary_csvfile
        )
        result = dh.generate_querents()

        self.assertListEqual(result, expect)

    def test_last_update(self):
        expect = self.datetime_now_str

        dh = handler.DataHandler(
            patients_csvfile=self.patients_csvfile,
            data_summary_csvfile=self.data_summary_csvfile,
            total_sickbeds=118
        )
        result = dh.generate_data()["lastUpdate"]

        self.assertEqual(result, expect)

    def __generate_null_data(self, start_date):
        datetime_now = datetime.datetime.now()
        end_date = datetime_now if datetime_now.hour >= 22 else \
            datetime_now - datetime.timedelta(days=1)

        null_data = []
        for i in self.__daterange(start_date, end_date):
            d = {
                "日付": i.strftime("%Y-%m-%d"),
                "小計": 0,
            }
            null_data.append(d)

        return null_data

    def __daterange(self, start_date, end_date):
        for n in range((end_date - start_date).days + 1):
            yield start_date + datetime.timedelta(n)


if __name__ == "__main__":
    unittest.main()
