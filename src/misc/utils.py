# -*- coding: utf-8 -*-
# Module  : 
# Author  : fengfeng    
# Date    : 2018-10-02
# Version : 1.0
# Desc    : 主要是获取session 以及 日期处理



import time, datetime, calendar
import os, json, re
from datetime import timedelta
import web
from calendar import monthrange
def get_session_value(key, prefix=''):
    sess = web.ctx.session
    key = key + prefix

    return sess.get(key, {})


def set_session_value(key, value, prefix=''):
    sess = web.ctx.session
    key = key + prefix
    sess[key] = value




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



'''
    将时间戳转换成年月日时分格式
        
'''
def YMDHMS2TS(strdate):
    
    return time.mktime(time.strptime(strdate, '%Y-%m-%d %H:%M:%S'))


'''
    将时间戳转换成年月日时分格式
        
'''
def YMDHM2TS(strdate):
    
    return time.mktime(time.strptime(strdate, '%Y-%m-%d %H:%M'))

def YMDH2TS(strdate):
    
    return time.mktime(time.strptime(strdate, '%Y-%m-%d %H'))


'''
    将时间戳转换成年月日时分格式
        
'''
def YMD2TS(strdate, fmt='%Y-%m-%d'):
    return time.mktime(time.strptime(strdate, fmt))


def YM2TS(strdate):
    return time.mktime(time.strptime(strdate, '%Y-%m'))


def Y2TS(strdate):
    return time.mktime(time.strptime(strdate, '%Y'))

''' 
    将字符串转换成时间戳
'''
def STR2TS(strdate):
    if len(strdate) == 4:
        if strdate.find(':')>-1:
            return YMD2TS(strdate,'%H:%M')
        return Y2TS(strdate)
    elif len(strdate) == 7:
        return YM2TS(strdate)
    elif len(strdate) == 10:
        return YMD2TS(strdate)
    elif len(strdate) == 13:
        return YMDH2TS(strdate)
    elif len(strdate) == 16:
        return YMDHM2TS(strdate)
    elif len(strdate) == 19:
        return YMDHMS2TS(strdate)
    return 0
