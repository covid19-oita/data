import json
from data.domain.feed import Feed
import feedparser


class FeedApplicationService(object):
    @classmethod
    def dump_json(cls, max_feed=3):
        """
        max_feedの数だけfeedを生成します
        Args:
            max_feed (int): 返すfeedの最大数
        Returns:
            dict: 適切なフォーマットに処理されたfeed
            
        Note:
            entries[i].updated_parsed は 最終更新日時を9タプルで返します
            https://pythonhosted.org/feedparser/reference-entry-updated_parsed.html
        """
        url = "http://www.pref.oita.jp/rss/10/site-1000786.xml"
        parsed_feeds = feedparser.parse(url)
        dirty_feeds = parsed_feeds.entries[0:max_feed]
        new_itmes = {
            "newItems": [Feed(dirty_feed).to_dict() for dirty_feed in dirty_feeds]
        }
        with open("./json/news.json", "w") as fp:
            json.dump(new_itmes, fp, indent=2, ensure_ascii=False)
