class Patients(object):
    def __init__(self) -> None:
        self.release_date: str
        self.residence: str
        self.age: str
        self.sex: str
        self.is_better: str
        self.date: str

    def to_dict(self):
        return {
            "リリース日": self.release_date,
            "居住地": self.residence,
            "年代": self.age,
            "性別": self.sex,
            "退院": self.is_better,
            "date": self.date,
        }


class Demographic(object):
    def __init__(self) -> None:
        self._u_10s: int
        self._10s: int
        self._20s: int
        self._30s: int
        self._40s: int
        self._50s: int
        self._60s: int
        self._70s: int
        self._80s: int
        self._o_90s: int

    def to_dict(self) -> dict:
        return {
            "10代未満": self._u_10s,
            "10代": self._10s,
            "20代": self._20s,
            "30代": self._30s,
            "40代": self._40s,
            "50代": self._50s,
            "60代": self._60s,
            "70代": self._70s,
            "80代": self._80s,
            "90代以上": self._o_90s,
        }


class SickbedsSummary(object):
    def __init__(self) -> None:
        self.hospitalized_patienst: int
        self.sickbeds_count: int
    def to_dict(self):
        return {
            "入院患者数": self.hospitalized_patienst,
            "病床数": self.sickbeds_count
        }


## 相談件数
class Qurents(object):
    def __init__(self) -> None:
        # "日付"
        self.date: str
        # "小計"
        self.amount: int

    def to_dict(self):
        return {
            "日付": self.date,
            "小計": self.amount,
        }
