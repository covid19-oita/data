import feedparser
from datetime import datetime


class RSSHandler:
    def __init__(self):
        self.news = {
            "newsItems": []
        }

    def generate_news(self, rss_url, itemCount=3):
        self.feedparser = feedparser.parse(rss_url)

        newsItems = []
        for entry in self.feedparser.entries[0:itemCount]:
            newsItems.append(
                {
                    "date": datetime(*entry.updated_parsed[:6]).strftime("%Y-%m-%d"),
                    "url": entry.link,
                    "text": entry.title.replace("\u3000", " "),
                }
            )
        self.news["newsItems"] = newsItems

        return self.news
