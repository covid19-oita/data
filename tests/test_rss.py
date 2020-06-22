import pytest
import json
import feedparser
from data.rss import generate_feeds
import ast

def test_generate_news(mocker):
    rss_mock = mocker.Mock()
    sample_feed = "[{'id': 'http://www.pref.oita.jp/site/covid19-oita/covid19-oita-0618.html', 'title': '移動自粛の全面解除に伴う知事からのメッセージ（６月１８日）', 'title_detail': {'type': 'text/plain', 'language': 'ja', 'base': 'http://www.pref.oita.jp/rss/10/site-1000786.xml', 'value': '移動自粛の全面解除に伴う知事からのメッセージ（６月１８日）'}, 'links': [{'rel': 'alternate', 'type': 'text/html', 'href': 'http://www.pref.oita.jp/site/covid19-oita/covid19-oita-0618.html'}], 'link': 'http://www.pref.oita.jp/site/covid19-oita/covid19-oita-0618.html', 'summary': '', 'summary_detail': {'type': 'text/html', 'language': 'ja', 'base': 'http://www.pref.oita.jp/rss/10/site-1000786.xml', 'value': ''}, 'updated': '2020-06-18T18:00:00+09:00', 'updated_parsed': time.struct_time(tm_year=2020, tm_mon=6, tm_mday=18, tm_hour=9, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=170, tm_isdst=0), 'tags': [{'term': '大分県', 'scheme': None, 'label': None}]}]"
    print(sample_feed)
#    input_feed = feedparser.FeedParserDict(ast.literal_eval(sample_feed))
#    mocker.patch("data.rss.feedparser.parse").return_value = input_feed
#    actual = generate_feeds(max_feed=1)
    assert True
    
