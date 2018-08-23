import datetime



class GlobalEnv:
    def __init__(self):
        self.code = '00001'
        self.freq = 'D'
        self.date = datetime.datetime.now()
        self.ref=0


ENV = GlobalEnv()


# todo 形参默认值引用全局变量引用不到
def set_current(code_new='', freq_new='', date_new=''):
    if code_new != "":
        ENV.code = code_new
    if freq_new != "":
        ENV.freq = freq_new
    if date_new != "":
        ENV.date = date_new
    print("set_current", ENV.code, ENV.freq, ENV.date)


def ser_ref(ref):
    ENV.ref = ref
