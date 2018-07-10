# -*- coding: utf-8 -*-
import time,datetime

# In: 将时间戳格式 输出时间戳
# tp   ts
# out :
#   时间戳
def getFormatterDate( tp=None,ts=None):
    if not ts:
        ts=int(time.time())
    t1 = time.localtime(float(ts))
    if not tp:
        tp="D"
    if tp == 'N':
        return ts
    elif tp == 'H':
        return int(time.mktime(datetime.datetime(t1[0], t1[1], t1[2], t1[3], 0, 0, 0).timetuple()))
    elif tp == 'D':
        return int(time.mktime(datetime.datetime(t1[0], t1[1], t1[2], 0, 0, 0, 0).timetuple()))
    elif tp == 'M':
        return int(time.mktime(datetime.datetime(t1[0], t1[1], 1, 0, 0, 0, 0).timetuple()))
    elif tp == 'Y':
        return int(time.mktime(datetime.datetime(t1[0], 1, 1, 0, 0, 0, 0).timetuple()))