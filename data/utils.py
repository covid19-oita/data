import csv
import json


def load_json_from_csv(file):
    """
    指定されたCSVファイルパスを読み込み、JSONデシリアライズします
    Args:
        file: CSVファイルパス
    Returns:
        Any: JSONデシリアライズされたオブジェクト
    """
    json_list = []
    with open(file, 'r', encoding='utf_8_sig') as f:
        for row in csv.DictReader(f):
            json_list.append(row)
    return json.loads(json.dumps(json_list))

def 
