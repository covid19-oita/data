from data.domain.utils import aggregate


def test_aggregate():
    l = [{"年代": "30代", "性別": "男性"}, {"年代": "20代", "性別": "男性"}]
    got = aggregate(l, "年代")
    want = {"20代": 1, "30代": 1}
    assert got == want
