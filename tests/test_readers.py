import pytest
import mock
from data.readers import FinancialReader


class TestFinancialReader(object):
    def test_read(self):
        fin_reader = FinancialReader()
        fin_reader.read()
        assert 1 == 1

