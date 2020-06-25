import feedparser
from datetime import datetime
import json


def _parse_feeds(max_feed):
    url = "http://www.pref.oita.jp/rss/10/site-1000786.xml"
    parsed_feeds = feedparser.parse(url)
    feeds = parsed_feeds.entries[0:max_feed]
    return feeds


def generate_feeds(max_feed=3):
    """
    max_feedの数だけurlのfeedを適切な形に変換します
    Args:
        max_feed (int): 返すfeedの最大数
    Returns:
        dict: 適切なフォーマットに処理されたfeed
        
    Note:
        entries[i].updated_parsed は 最終更新日時を9タプルで返します
        https://pythonhosted.org/feedparser/reference-entry-updated_parsed.html
    """
    feeds = _parse_feeds(max_feed)
    new_feeds = []
    for feed in feeds:
        year = feed.updated_parsed[0]
        month = feed.updated_parsed[1]
        day = feed.updated_parsed[2]
        new_feeds.append(
            {
                "date": datetime(year, month, day).strftime("%Y-%m-%d"),
                "url": feed.link,
                "text": feed.title.replace("\u3000", " "),
            }
        )
    return {"newsItems": new_feeds}
