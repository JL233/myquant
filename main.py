# 我们的那个p.submit(task,i)和map函数的原理类似。我们就
# 可以用map函数去代替。更减缩了代码
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import os, time, random


def task(n):
    print('[%s] is running' % os.getpid())
    time.sleep(random.randint(1, 3))  # I/O密集型的，，一般用线程，用了进程耗时长
    return n ** 2


if __name__ == '__main__':
    p = ProcessPoolExecutor()
    obj = p.map(task, range(10))
    p.shutdown()  # 相当于close和join方法
    print('=' * 30)
    print(obj)  # 返回的是一个迭代器
    print(list(obj))
