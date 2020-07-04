class SubsidySummary(object):
    def __init__(self) -> None:
        self.date: str
        self.application_count: int
        self.decisions_count: int

    def to_dict(self):
        return {
            "日付": self.date,
            "申請書提出件数": self.application_count,
            "支給決定件数": self.decisions_count,
        }


class LoanArchivementsByIndustry(object):
    def __init__(self, fin_series: dict, fin_type: dict) -> None:
        self.resutaurant: int
        self.service: int
        self.retail: int
        self.construction: int
        self.wholesale_trade: int
        self.accommodation: int
        self.manufacturing: int
        self.others: int

    def to_dict(self):
        return {
            "飲食業": self.resutaurant,
            "サービス業（宿泊除く）": self.service,
            "小売業": self.retail,
            "建設業": self.construction,
            "卸売業": self.wholesale_trade,
            "宿泊業": self.accommodation,
            "製造業": self.manufacturing,
            "その他": self.others,
        }
