# -*- coding: utf-8 -*-
'''
desc ：
  时间戳是自 1970 年 1 月 1 日（00:00:00 GMT）以来的秒数。它也被称为 Unix 时间戳（Unix Timestamp）。
  浏览器、后台、系统时间同步，本机时区获取时间戳
  闰秒：世界时，与原子时差异，处理：世界时调整
  datetime 获取时间，创建时间
  python 提供了一个 time 和 calendar 模块可以用于格式化日期和时间。
  time:模板更多的是处理时间戳
     ps:time.mktime 转换成时间戳格式
        time.strftime 转换成本地格式
        time.localtime 时间搓变时间tuple
'''
import time, datetime, calendar
from datetime import timedelta



'''
    根据给定时间戳获取对应的年份和月份

    @param ts 时间戳
'''
def getYearMonthByTimestamp(ts):

    t = time.localtime(float(ts))

    return t[0], t[1]

'''
    根据给定时间戳获取对应的月份和日期

    @param ts 时间戳
'''
def getMonthDayByTimestamp(ts):

    t = time.localtime(float(ts))

    return t[1], t[2]



'''
    获取当前月份的第一天和今天最后一秒
    ret 时间戳

'''
def getFirstEndDayOfCurMonth():
    cur = datetime.datetime.now()
    year = cur.year
    month = cur.month

    d = calendar.monthrange(year, month)

    start = int(time.mktime(datetime.datetime(year, month, 1, 0, 0, 0, 0).timetuple()))
    end   = int(time.mktime(datetime.datetime(year, month, d[1], 23, 59, 59, 0).timetuple()))

    return start, end

'''
    获取今年的第一天和最后一天最后一秒
    ret 时间戳

'''
def getFirstEndDayOfCurYear():
    cur = datetime.datetime.now()
    year = cur.year

    start = int(time.mktime(datetime.datetime(year, 1, 1, 0, 0, 0, 0).timetuple()))
    end   = int(time.mktime(datetime.datetime(year, 12, 31, 23, 59, 59, 0).timetuple()))

    return start, end



'''
    获取给定月份的第一天和最后一秒

'''
def getFirstEndDayOfMonth(year, month):
    d = calendar.monthrange(year, month)

    start = int(time.mktime(datetime.datetime(year, month, 1, 0, 0, 0, 0).timetuple()))
    end   = int(time.mktime(datetime.datetime(year, month, d[1], 23, 59, 59, 0).timetuple()))

    return start, end





'''
    比较两个时间戳是否为同一天

    @param ts 时间戳
    @return true false
'''
def isSameDay(ts1, ts2):
    t1 = time.localtime(float(ts1))
    t2 = time.localtime(float(ts2))

    return (t1[0] == t2[0]) & (t1[1] == t2[1]) & (t1[2] == t2[2])


'''
    将时间戳转换成年月日时

'''
def YMD(ts, fmt='%Y-%m-%d'):
    return time.strftime(fmt.encode('utf-8'), time.localtime(float(ts))).decode('utf-8')

def D(ts, fmt='%d'):
    return time.strftime(fmt, time.localtime(float(ts)))

def M(ts, fmt='%m'):
    return time.strftime(fmt, time.localtime(float(ts)))

'''
  时间 +   - 月份    时间戳格式 精确到 天
    日期格式精度与日期精度相同

'''
def add_months(dt,months):
    if isinstance(dt, int) or isinstance(dt, float):
        st=time.localtime(dt)
        return int(time.mktime(add_months(datetime.datetime(st[0],st[1], st[2], 0, 0, 0, 0),months).timetuple()))
    else:
        month = dt.month - 1 + months
        year = dt.year + month / 12
        month = month % 12 + 1
        day = min(dt.day,calendar.monthrange(year,month)[1])
        return dt.replace(year=year, month=month, day=day)

'''
判断是否为闰年
'''
def isLeapYear(y):
    '''
    判断是否为闰年
    '''
    if y%400==0 or (y%4==0 and y%100!=0):
        return True;
    else:
        return False;


def getDayCountByYear(y):
    '''
    获取年的天数
    '''
    if isLeapYear(y):
        return 366;
    else:
        return 365;

def getDayCount(y=None,m=None):
    '''
    获取当月的天数
    '''
    cur = datetime.datetime.now()
    if not y:
        y=cur.year
    if not m:
        m=cur.month
    m1 = [1,3,5,7,8,10,12]
    m2 = [4,6,9,11]
    if m in m1:
        return 31
    elif m in m2:
        return 30
    else:
        d = 28
        if isLeapYear(y):
            d=29
        return d

def getTMFromStr(ss,fmt= "%Y-%m-%d %H:%M:%S"):
    timeArray = time.strptime(ss, fmt)
    return int(time.mktime(timeArray))

print "test"
def test():
  print u"当前时间时间戳 s 以及毫秒"
  print int(time.time())
  print time.time()
  print u"--datetime.datetime.now()-----------返回的是时间类型%s" %(datetime.datetime.now());
  print u"获取年度"
  print  datetime.datetime.now().year;
  print u"获取今天几号------------------%s"%(datetime.datetime.now().day)



  print u"----获取星期-今天星期几----星期1 是 0-----------%s"%(datetime.datetime.now().weekday())


  (a,b)= getFirstEndDayOfCurYear()
  print a
  print b

  print u"获取当年第一天的时间戳，以及最后一秒的时间戳"
  print  getFirstEndDayOfCurYear()[0]
  print u"获取去年年第一天的时间戳,及最后一天"
  print  add_months(getFirstEndDayOfCurYear()[0],-12)
  print  getFirstEndDayOfCurYear()[0]-1

  print u"获取给定时间的时间戳"
  print getTMFromStr("2013-10-10 23:20:10");



  print u"获取当月第一天，及最后一秒"
  print getFirstEndDayOfCurMonth()[1]


  print u"获取给定月份的第一天和最后一秒****"
  print getFirstEndDayOfMonth(2017,12)
  print u"获取今天的时间数组****"
  dt = datetime.datetime.now().timetuple()
  print u"获取今天开始的时间戳****"
  day = int(time.mktime(datetime.datetime(dt[0], dt[1], dt[2], 0, 0, 0, 0).timetuple()))
  print u"获取今天开始的时间戳 or "
  print add_months(time.time(),0)
  print dt
  print day

  print getYearMonthByTimestamp(time.time())
  print getYearMonthByTimestamp(1514736000)
test()
