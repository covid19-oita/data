import json
import feedparser
from data.rss import _parse_feeds, generate_feeds
from mock import Mock


def test_generate_news():
    sample_feed = """
    [
    {
        "id":"http://www.pref.oita.jp/site/covid19-oita/covid19-oita-0618.html",
        "title":"移動自粛の全面解除に伴う知事からのメッセージ（６月１８日）",
        "title_detail":{
            "type":"text/plain",
            "language":"ja",
            "base":"http://www.pref.oita.jp/rss/10/site-1000786.xml",
            "value":"移動自粛の全面解除に伴う知事からのメッセージ（６月１８日）"
        },
        "links":[
            {
                "rel":"alternate",
                "type":"text/html",
                "href":"http://www.pref.oita.jp/site/covid19-oita/covid19-oita-0618.html"
            }
        ],
        "link":"http://www.pref.oita.jp/site/covid19-oita/covid19-oita-0618.html",
        "summary":"",
        "summary_detail":{
            "type":"text/html",
            "language":"ja",
            "base":"http://www.pref.oita.jp/rss/10/site-1000786.xml",
            "value":""
        },
        "updated":"2020-06-18T18:00:00+09:00",
        "updated_parsed":[
            2020,
            6,
            18,
            9,
            0,
            0,
            3,
            170,
            0
        ],
        "tags":[
            {
                "term":"大分県",
                "scheme":null,
                "label":null
            }
        ]
    },
    {
        "id":"http://www.pref.oita.jp/site/covid19-oita/covid19-pcr.html",
        "title":"大分県におけるPCR等検査実施人数及び患者状況（R2.6.24  17時30分更新）",
        "title_detail":{
            "type":"text/plain",
            "language":"ja",
            "base":"http://www.pref.oita.jp/rss/10/site-1000786.xml",
            "value":"大分県におけるPCR等検査実施人数及び患者状況（R2.6.24  17時30分更新）"
        },
        "links":[
            {
                "rel":"alternate",
                "type":"text/html",
                "href":"http://www.pref.oita.jp/site/covid19-oita/covid19-pcr.html"
            }
        ],
        "link":"http://www.pref.oita.jp/site/covid19-oita/covid19-pcr.html",
        "summary":"",
        "summary_detail":{
            "type":"text/html",
            "language":"ja",
            "base":"http://www.pref.oita.jp/rss/10/site-1000786.xml",
            "value":""
        },
        "updated":"2020-06-24T17:00:00+09:00",
        "updated_parsed":[
            2020,
            6,
            24,
            8,
            0,
            0,
            2,
            176,
            0
        ],
        "tags":[
            {
                "term":"健康づくり支援課",
                "scheme":null,
                "label":null
            }
        ]
    },
    {
        "id":"http://www.pref.oita.jp/site/covid19-oita/jinnkennsingatacorona.html",
        "title":"新型コロナウイルス感染症に関連する人権への配慮について",
        "title_detail":{
            "type":"text/plain",
            "language":"ja",
            "base":"http://www.pref.oita.jp/rss/10/site-1000786.xml",
            "value":"新型コロナウイルス感染症に関連する人権への配慮について"
        },
        "links":[
            {
                "rel":"alternate",
                "type":"text/html",
                "href":"http://www.pref.oita.jp/site/covid19-oita/jinnkennsingatacorona.html"
            }
        ],
        "link":"http://www.pref.oita.jp/site/covid19-oita/jinnkennsingatacorona.html",
        "summary":"",
        "summary_detail":{
            "type":"text/html",
            "language":"ja",
            "base":"http://www.pref.oita.jp/rss/10/site-1000786.xml",
            "value":""
        },
        "updated":"2020-06-24T00:00:00+09:00",
        "updated_parsed":[
            2020,
            6,
            23,
            15,
            0,
            0,
            1,
            175,
            0
        ],
        "tags":[
            {
                "term":"人権尊重・部落差別解消推進課",
                "scheme":null,
                "label":null
            }
        ]
    }
    ]
    """
    _parse_feeds = Mock(return_value=sample_feed)
    got = generate_feeds(max_feed=1)
    wants = {
        'newsItems': [
            {
                'date': '2020-06-18',
                'url': 'http://www.pref.oita.jp/site/covid19-oita/covid19-oita-0618.html',
                'text': '移動自粛の全面解除に伴う知事からのメッセージ（６月１８日）',
            }
        ]
    }
    assert wants == got
