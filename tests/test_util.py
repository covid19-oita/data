import pytest


@pytest.fixture
def csv_factory():
    def factory(tmpdir):
        tmp_json = tmpdir.mkdir("test").join("data.json")
        tmp_json.write("content")
        tmp_json.close()
        return temp_json

    return factory


def test_load_json_from_csv(csv_factory):
    pass

