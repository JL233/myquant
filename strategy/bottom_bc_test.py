import unittest
from datetime import timedelta

from strategy.bottom_bc import bottom_bc
from env import set_current, ENV
from tdx.func import REF


class bottom_bj_test(unittest.TestCase):
    def test(self):
        set_current("000001", "5")
        self.assertEqual(bottom_bc(), False)
        set_current(date_new=ENV.date - timedelta(days=4))
        self.assertEqual(REF(bottom_bc, 12), True)
        self.assertEqual(REF(bottom_bc, 12), True)
        self.assertEqual(REF(bottom_bc, 12), True)
        self.assertEqual(REF(bottom_bc, 13), False)
