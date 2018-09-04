from common.env import g


def condition(func):
    def wrapper(*args, **kw):
        result = func(*args, **kw)
        return g.ENV.date, func.__name__, g.ENV.freq, result
    return wrapper
