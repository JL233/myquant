import unittest

from tdx.func import REF


class top_bj_test(unittest.TestCase):
    def test(self):
        set_current("000001", "5")
        self.assertEqual(top_bc(), False)
        set_current(date_new=g.ENV.date - timedelta(days=4))
        self.assertEqual(REF(top_bc, 11), False)
        self.assertEqual(REF(top_bc, 12), True)
        self.assertEqual(REF(top_bc, 12), True)
        self.assertEqual(REF(top_bc, 13), False)
