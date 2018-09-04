import concurrent
import copy
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor

from pandas import DataFrame

from common.env import Global, g


class TestThread(unittest.TestCase):
    result_done=False
    f1=None
    def test_through(self):
        global f1
        result_df = DataFrame(columns=['买卖', '级别', "信号"])

        g.ENV = Global()
        g.ENV.freq = "5min"
        print(id(g.ENV))
        self.executor = ThreadPoolExecutor(max_workers=5)
        f1 = self.executor.submit(self.buy_cond2, g.ENV)
        f1.add_done_callback(self.done)
        for future in concurrent.futures.as_completed([f1]):
            res = future.result()
            if res['ok']:
                print(res)

    def buy_cond2(self, e):

        print(id(e))
        g.ENV = copy.copy(e)
        self.executor.submit(self.done, g.ENV)
        g.ENV.freq = e.freq
        time.sleep(3)
        print(id(g.ENV))
        return False

    def done(self, res):
        global f1
        print(f1.done())
        print(id(g.ENV))

        print("is add_record in mainThread：%r", isinstance(threading.current_thread(), threading._MainThread))

        result = res.result()
        res = {'ok': res, 'date': g.ENV.freq}
