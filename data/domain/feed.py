from datetime import datetime
from feedparser import FeedParserDict


class Feed(object):
    def __init__(self, dirty_feed: FeedParserDict) -> None:
        self.date: str
        self.url: str
        self.text: str
        year = dirty_feed.updated_parsed[0]
        month = dirty_feed.updated_parsed[1]
        day = dirty_feed.updated_parsed[2]
        self.date = datetime(year, month, day).strftime("%Y-%m-%d")
        self.url = dirty_feed.link
        self.text = dirty_feed.title.replace("\u3000", " ")

    def to_dict(self):
        return dict(date=self.date, url=self.url, text=self.text)
