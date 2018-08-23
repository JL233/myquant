import unittest

from fetch_kdata import init_k_data


class FetchKdataTest(unittest.TestCase):
    def test_init_kdata_5(self):
        code = "000001"
        ktype = "5"
        init_k_data(code, ktype, day=5)
    def test_init_kdata_60(self):
        code = "000001"
        ktype = "60"
        init_k_data(code, ktype, day=5)
