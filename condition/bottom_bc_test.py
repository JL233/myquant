import datetime
import unittest

from common.env import Global, g, set_current
from condition.bottom_bc import bottom_bc
from tdx.func import REF


class bottom_bj_test(unittest.TestCase):
    def setUp(self):
        g.ENV = Global()
        g.ENV = Global()
        g.ENV.code = "000001"
        g.ENV.asset = 'INDEX'
        print("do something before test.Prepare g.ENVironment.")

    def tearDown(self):
        print("do something after test.Clean up.")

    def test(self):
        g.ENV.date = datetime.datetime.strptime("2018-08-29 10:30:00", '%Y-%m-%d %H:%M:%S')
        g.ENV.freq = '5min'
        self.assertEqual(bottom_bc(g.ENV), False)
        self.assertEqual(REF(bottom_bc, 2), False)
        self.assertEqual(REF(bottom_bc, 3), False)
        self.assertEqual(REF(bottom_bc, 4), True)
        self.assertEqual(REF(bottom_bc, 5), False)
