# -*- coding: utf-8 -*-
# Module  : 
# Author  : Liujinxiao
# Date    : 2014-09-15
# Version : 1.0

import time, datetime, calendar
import os, json, re
from datetime import timedelta
import web
from calendar import monthrange
from bson import ObjectId


NUMBER_FORMAT = '%.1f'

POWER_RATE_MUCH=[]

'''计算电费逻辑'''
def power_rate_condtion_much(st_time,et_time,val):
    d = '2000-01-01 '
    if len(POWER_RATE_MUCH) <=0:
        import service
        for c in list(service.biz.power_rate.items()):
            c['st_time']=int(YMDHMS2TS(d+c['st_time']+':00'))
            c['et_time']=int(YMDHMS2TS(d+c['et_time']+':00'))
            POWER_RATE_MUCH.append(c)
        if len(POWER_RATE_MUCH) <=0:
            POWER_RATE_MUCH.append({'st_time':int(YMDHMS2TS(d+'00:00:00')),'et_time':int(YMDHMS2TS(d+'23:59:59')),'much':10})
    for b in POWER_RATE_MUCH:
        st=int(YMDHMS2TS(d+st_time+':00'))
        et=int(YMDHMS2TS(d+et_time+':00'))
        if st >= b['st_time'] and et <=b['et_time']:
            if float(val) == 0 or (float(val) == 0 and b['much'] == 0):
                return 0
            
            return float(val)*b['much']
    return 0
        

'''
转换时间
'''
def query_time(date,starttime,endtime): 
  
    begin, end = (date+' '+starttime+':00'), (date+' '+endtime+':00')
   
    begin = datetime.datetime.strptime(begin, '%Y-%m-%d %H:%M:%S')
    end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
   
    if begin >= end: end+=timedelta(1)
   
    st= int(time.mktime(begin.timetuple()))
    et= int(time.mktime(end.timetuple()))+1
    return st,et

def number_format(v, fmt=NUMBER_FORMAT, retStr = False):
    
    if retStr:
        return v if v is None else (fmt %v)
    else:
        return v if v is None else float(fmt %v)
    
'''
数组求平均数
'''  
def avg_arr(arr):
    if arr:
        ilen=len(arr)  
        isum=0
        for v in arr:
            if v:
                v=float(v)
                isum=isum+v 
        return round( isum/ilen,3)    
    else:
        return None

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
    获取上一个月的第一天和最后一天
        
'''
def getFirstEndDayOfLastMonth():
    cur = datetime.datetime.now()
    year = cur.year
    month = cur.month
    
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    
    d = calendar.monthrange(year, month)
    
    start = int(time.mktime(datetime.datetime(year, month, 1, 0, 0, 0, 0).timetuple()))
    end   = int(time.mktime(datetime.datetime(year, month, d[1], 23, 59, 59, 0).timetuple()))
    
    return start, end

def getFirstEndDayOfLastMonth4Month(year, month):
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    
    d = calendar.monthrange(year, month)
    
    start = int(time.mktime(datetime.datetime(year, month, 1, 0, 0, 0, 0).timetuple()))
    end   = int(time.mktime(datetime.datetime(year, month, d[1], 23, 59, 59, 0).timetuple()))
    
    return start, end


'''
    获取当前月份的第一天和今天
        
'''
def getFirstNowDayOfCurMonth():
    cur = datetime.datetime.now()
    year = cur.year
    month = cur.month
    
    d = calendar.monthrange(year, month)
    
    start = int(time.mktime(datetime.datetime(year, month, 1, 0, 0, 0, 0).timetuple()))
    end   = int(time.mktime(datetime.datetime(year, month, d[1], 23, 59, 59, 0).timetuple()))
    
    return start, end


def getFirstEndDayOfCurWeek():
    cur = datetime.datetime.now()
    
    start = int(time.mktime(datetime.datetime(cur.year, cur.month, cur.day, 0, 0, 0).timetuple()))
    start = start - 86400 * cur.weekday()
    end = start + 86400 * 6 - 1
    
    return start, end
    

def getFirstEndDayOfCurMonth():
    cur = datetime.datetime.now()
    year = cur.year
    month = cur.month
    
    d = calendar.monthrange(year, month)
    
    start = int(time.mktime(datetime.datetime(year, month, 1, 0, 0, 0, 0).timetuple()))
    end   = int(time.mktime(datetime.datetime(year, month, d[1], 23, 59, 59, 0).timetuple()))
    
    return start, end


def getFirstEndDayOfCurYear():
    cur = datetime.datetime.now()
    year = cur.year
    
    start = int(time.mktime(datetime.datetime(year, 1, 1, 0, 0, 0, 0).timetuple()))
    end   = int(time.mktime(datetime.datetime(year, 12, 31, 23, 59, 59, 0).timetuple()))
    
    return start, end


'''
    获取给定月份的第一天和最后一天
        
'''
def getFirstEndDayOfMonth(year, month):
    d = calendar.monthrange(year, month)
    
    start = int(time.mktime(datetime.datetime(year, month, 1, 0, 0, 0, 0).timetuple()))
    end   = int(time.mktime(datetime.datetime(year, month, d[1], 23, 59, 59, 0).timetuple()))
    
    return start, end


'''
    获取当前年份的第一天和今天
        
'''
def getFirstLastDayOfYear(year):
    start = int(time.mktime(datetime.datetime(year, 1, 1, 0, 0, 0, 0).timetuple()))
    end   = int(time.mktime(datetime.datetime(year, 12, 31, 23, 59, 59, 0).timetuple()))
    
    return start, end


'''
    获取当前月份的第一天和今天
        
'''
def getStartEndOfOneDay(ts):
    t = time.localtime(float(ts))
    
    start = int(time.mktime(datetime.datetime(t[0], t[1], t[2], 0, 0, 0, 0).timetuple()))
    end   = int(time.mktime(datetime.datetime(t[0], t[1], t[2], 23, 59, 59, 0).timetuple()))
    
    return start, end


'''
    获取某天和过去 N天的时间
    @param ts 某一天
    @param partDays 过去 N天 
'''
def getLastPartDay(ts=time.time(), partDays=30):
    
    start = ts - timedelta(days=partDays).total_seconds()
    #end   = int(ts)
    
    return start#, end


'''
    根据给定时间戳获取对应的年份和月份
        
    @param ts 时间戳
'''
def isSameDay(ts1, ts2):
    t1 = time.localtime(float(ts1))
    t2 = time.localtime(float(ts2))
    
    return (t1[0] == t2[0]) & (t1[1] == t2[1]) & (t1[2] == t2[2])


'''
    根据给定时间获取对应的一个收费周期    
        
    @param dt 时间戳
'''
def getCycleDays4CurDate(cur, step):
    
    maxDay = [31,28,31,30,31,30,31,31,30,31,30,31]
    
    year  = cur[0]
    month = cur[1]
    day   = cur[2]
    
    startYear  = year
    startMonth = month - step
    startDay   = day
    
    if startMonth < 1:
        _startMonth = (- startMonth)
        length = (_startMonth - _startMonth % 12) / 12 + 1
        
        startYear -= length
        startMonth = month - step + 12 * length
        
    if startMonth == 2:
        if startDay == 29:
            if (startYear%4 == 0 and (startYear%100 != 0 or startYear%400 == 0)):
                pass
            else:
                startMonth += 1
                startDay = 1
        elif day > 29:
            startMonth += 1
            startDay = 1
    
    else:
        if startDay == 31:
            if startDay > maxDay[startMonth - 1]:
                startMonth += 1
                startDay = 1
                
    if day == 1:
        if month == 1:
            year -= 1
            month = 12
            day   = 31
        elif month == 3:
            month = 2
            day   = 28
            if (startYear%4 == 0 and (startYear%100 != 0 or startYear%400 == 0)):
                day += 1
        else:
            month -= 1
            day    = maxDay[month - 1]
    else:
        day -= 1
        
        
    start = int(time.mktime(datetime.datetime(startYear, startMonth, startDay, 0, 0, 0, 0).timetuple()))
    end   = int(time.mktime(datetime.datetime(year, month, day, 23, 59, 59, 0).timetuple()))
    
    return start, end


'''
    同比时间段  
        
    @param start 起始时间
    @param end 结束时间
'''
def getLastYearSamePeriod(start, end):
    
    start = time.localtime(float(start))
    end   = time.localtime(float(end))
    
    #同比
    lyStartYear  = start[0] - 1
    lyStartMonth = start[1]
    lyStartDay   = start[2]
    
    if lyStartDay == 29 and lyStartMonth == 2:
        if (lyStartYear%4 == 0 and (lyStartYear%100 != 0 or lyStartYear%400 == 0)):
            pass
        else:
            lyStartMonth += 1
            lyStartDay = 1
    
    
    lyEndYear  = end[0] - 1
    lyEndMonth = end[1]
    lyEndDay   = end[2]
    
    if lyEndDay == 29 and lyEndMonth == 2:
        if (lyEndYear%4 == 0 and (lyEndYear%100 != 0 or lyEndYear%400 == 0)):
            pass
        else:
            lyEndDay -= 1
    
    
    lyStart = int(time.mktime(datetime.datetime(lyStartYear, lyStartMonth, lyStartDay, 0, 0, 0, 0).timetuple()))
    lyEnd   = int(time.mktime(datetime.datetime(lyEndYear, lyEndMonth, lyEndDay, 23, 59, 59, 0).timetuple()))
    
    return lyStart, lyEnd


'''
    环比时间段  
        
    @param start 起始时间
    @param end 结束时间
'''
def getLastMonthSamePeriod(start, end):
    
    maxDay = [31,29,31,30,31,30,31,31,30,31,30,31]
    
    start = time.localtime(float(start))
    end   = time.localtime(float(end))
    
    #同比
    lmStartYear  = start[0]
    lmStartMonth = start[1] - 1
    lmStartDay   = start[2]
    
    if lmStartMonth == 0:
        lmStartYear -= 1 
        lmStartMonth = 12
        
    if lmStartDay > maxDay[lmStartMonth - 1]:
        lmStartDay = maxDay[lmStartMonth - 1]
    
    if lmStartDay == 29 and lmStartMonth == 2:
        if (lmStartYear%4 == 0 and (lmStartYear%100 != 0 or lmStartYear%400 == 0)):
            pass
        else:
            lmStartDay -= 1
        
    lmEndYear  = end[0]
    lmEndMonth = end[1] - 1
    lmEndDay   = end[2]
    
    if lmEndMonth == 0:
        lmEndYear -= 1 
        lmEndMonth = 12

    if lmEndDay > maxDay[lmEndMonth - 1]:
        lmEndDay = maxDay[lmEndMonth - 1]

    if lmEndDay == 29 and lmEndMonth == 2:
        if (lmEndYear%4 == 0 and (lmEndYear%100 != 0 or lmEndYear%400 == 0)):
            pass
        else:
            lmEndDay -= 1
    
    lmStart = int(time.mktime(datetime.datetime(lmStartYear, lmStartMonth, lmStartDay, 0, 0, 0, 0).timetuple()))
    lmEnd   = int(time.mktime(datetime.datetime(lmEndYear, lmEndMonth, lmEndDay, 23, 59, 59, 0).timetuple()))
    
    return lmStart, lmEnd


'''
    本旬时间段  
        
    @param start 起始时间
    @param end 结束时间
'''
def getStartEndOfThisPeriod(date=None):
    
    now = time.time() if date is None else date
    year, month = getYearMonthByTimestamp(now)
    start, end = getFirstEndDayOfMonth(year, month)
    
    tll = time.localtime(now)
    day = tll[2]
 
    if day <= 10:
        end = getLastPartDay(start, -10) - 1
    elif day <= 20:
        start = getLastPartDay(start, -10)
        end = getLastPartDay(start, -20) - 1
    else:
        start = getLastPartDay(start, -20)
        
    return start, end

'''
    获取当前月份的第一天和今天
        
'''
def splitStrDate2Detail(ts):
    t = time.localtime(float(ts))
    
    return '%4d-%02d-%02d'%(t[0], t[1], t[2]), t[3], t[4], t[5]


'''
    将时间戳转换成时分格式
        
'''
def HM(ts):
    
    return time.strftime('%H:%M', time.localtime(float(ts)))


'''
    将时间戳转换成年月日时分格式
        
'''
def YMDHM(ts):
    
    return time.strftime('%Y-%m-%d %H:%M', time.localtime(float(ts)))

def YMDH(ts):
    
    return time.strftime('%Y-%m-%d %H', time.localtime(float(ts)))


def MDHM(ts):
    
    return time.strftime('%m-%d %H:%M', time.localtime(float(ts)))


def HMS(ts):
    
    return time.strftime('%H:%M:%S', time.localtime(float(ts)))

'''
    将时间戳转换成年月日时分格式
        
'''
def yMDHM(ts):
    
    return time.strftime('%y/%m/%d %H:%M', time.localtime(float(ts)))

'''
    将时间戳转换成年月日时
        
'''
def YMD(ts, fmt='%Y-%m-%d'):
    return time.strftime(fmt.encode('utf-8'), time.localtime(float(ts))).decode('utf-8')

def D(ts, fmt='%d'):
    return time.strftime(fmt, time.localtime(float(ts)))

def M(ts, fmt='%m'):
    return time.strftime(fmt, time.localtime(float(ts)))

def C_MD(ts):
    
    tll = time.localtime(float(ts))
    
    return u'%s月%s日'%(tll[1], tll[2])

'''
    将时间戳转换成年月日时
        
'''
def YM(ts):
    
    return time.strftime('%Y-%m', time.localtime(float(ts)))

def Y(ts):
    
    return time.strftime('%Y', time.localtime(float(ts)))


def MD(ts):
    
    return time.strftime('%m-%d', time.localtime(float(ts)))


def Ts2Day(ts):
    
    d= time.strftime('%Y-%m-%d', time.localtime(float(ts)))
    return time.mktime(time.strptime(d, '%Y-%m-%d'))

def S_YM_C(ts):
    
    st = YM(ts)
    
    st = st.replace('-', u'年')
    st += u'月'
    
    return st


'''
    将时间戳转换成年月日时
        
'''
def LT_YMD(lt):
    
    return time.strftime('%Y-%m-%d', lt)

'''
    将时间戳转换成年月日时分格式
        
'''
def YMDHMS(ts):
    if ts:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))
    return ''

def YMDHMSm(ts):
    t = float(ts / 1000)
    m = int(ts % 1000)
    
    return '%s %.3d'%(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t)), m)


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

'''
输入字符串格式时间如2-16-06,以时间戳格式输出该月第一天跟最后一天时间
'''
def getStartAndEndDayOfMonth(curdate, ty=None):
    cur = curdate.split('-')
    start = cur[0] + '-' + cur[1] + '-' + '01'
    end = cur[0] + '-' + cur[1] + '-' + str(monthrange(int(cur[0]), int(cur[1]))[1])
    if ty == "str":
        return start, end
    else:
        return YMD2TS(start), YMD2TS(end)

'''
    获取给定日期的前一天
        
'''
def S_YMD2LT(strdate):
    t = time.strptime(strdate, '%Y-%m-%d')
    t = int(time.mktime(t))
    t = time.localtime(float(t))
    
    return t


'''
    获取给定日期的前一天
        
'''
def S_YMD2LT2(strdate):
    t = time.strptime(strdate, '%Y%m%d')
    t = int(time.mktime(t))
    t = time.localtime((t))
    
    return t


'''
    获取给定月份的第一天
        
'''
def FD_YM2ST(strmonth):
    t = time.localtime(time.mktime(time.strptime(strmonth, '%Y-%m')))
    
    start = time.mktime(datetime.datetime(t[0], t[1], 1, 0, 0, 0, 0).timetuple())
    
    return start


'''
    获取给定月份的第一天
        
'''
def YMDHM2ST(strmonth):
    t = time.localtime(time.mktime(time.strptime(strmonth, '%Y-%m-%d %H:%M')))
    
    start = time.mktime(datetime.datetime(t[0], t[1], t[2], t[3], t[4], 0, 0).timetuple())
    
    return start


'''
    获取给定月份的最后一天
        
'''
def LD_YM2ST(strmonth):
    t = time.localtime(time.mktime(time.strptime(strmonth, '%Y-%m')))
    d = calendar.monthrange(t[0], t[1])
    
    end = time.mktime(datetime.datetime(t[0], t[1], d[1], 23, 59, 59, 0).timetuple())
    
    return end


'''
    获取给定日期的前一天
        
'''
def getLast4OneStrDay(dt):
    t = time.strptime(dt, '%Y-%m-%d')
    t = int(time.mktime(t))
    t = t - timedelta(days=1).total_seconds()
    t = time.localtime(float(t))
    
    return time.strftime('%Y-%m-%d', t)


'''
    获取给定的月份范围
        
'''
def getMonthRange(startMonth, endMonth):
    
    monthRange = []
    
    start = time.localtime(time.mktime(time.strptime(startMonth, '%Y-%m')))
    startY, startM = start[0], start[1]
    
    end = time.localtime(time.mktime(time.strptime(endMonth, '%Y-%m')))
    endY, endM = end[0], end[1]
    
    length = (endY - startY) * 12 + endM - startM + 1
    
    for i in range(length):
        
        year  = startY + (startM + i) / 12
        month = (startM + i) % 12 if (startM + i) % 12 != 0 else 12
        
        monthRange.append(('%d-%0.2d'%(year, month)))
    

    return monthRange

def getMonCountbyTs(ts1,ts2):
    dt1=datetime.datetime.fromtimestamp(ts1)
    dt2=datetime.datetime.fromtimestamp(ts2)
    return (dt2.year-dt1.year)*12+(dt2.month-dt1.month)

'''
    获取上年的同一时期
'''
def LYSP_YM(strmonth):
  
    t = time.localtime(time.mktime(time.strptime(strmonth, '%Y-%m')))
    
    return '%d-%0.2d'%(t[0]-1, t[1])

'''
    获取上年的同一天
        
'''
def LYSP_YMD(strmonth):
  
    t = time.localtime(time.mktime(time.strptime(strmonth, '%Y-%m-%d')))
    
    if t[0] == 2 and t[1] == 29:
      t[1] = 28
    
    return '%d-%0.2d-%0.2d'%(t[0]-1, t[1], t[2])

'''
    获取上月的同一时期
        
'''
def LMSP_YM(strmonth):
  
    t = time.localtime(time.mktime(time.strptime(strmonth, '%Y-%m')))
    year, month = t[0], t[1] - 1
    
    if month == 0:
        year, month = (t[0] - 1), 12
    
    return '%d-%0.2d'%(year, month)
    

'''
    获取昨天
        
'''
def LMSP_YMD(ymd):
  
    ymd = datetime.datetime.fromtimestamp(time.mktime(time.strptime(ymd, '%Y-%m-%d')))
    ymd = ymd - datetime.timedelta(days = 1)
    return time.strftime('%Y-%m-%d', ymd.timetuple())
    

'''
  系统用时标
'''
def HM_DHM(mx):
  
    dt = datetime.datetime.fromtimestamp(mx)
    now = datetime.datetime.now()
    if dt.date() == now.date():
        dt = '%02d:%02d'%(dt.hour,dt.minute) 
    else:
        dt = '%02d-%02d %02d:%02d'%(dt.month,dt.day,dt.hour,dt.minute)
    
    return dt

'''
    计算两个时间相差天数
        
'''
def compareDaysByDiffDate(start, end):
    
    return int((end - start)/86400) # 24*60*60


'''
    获取给定的月份范围
        
'''
def getTCompareMonth(ym):
    
    monthRange = []
    
    start = time.localtime(time.mktime(time.strptime(ym, '%Y-%m')))
    startY, startM = start[0], start[1]
    
    end = time.localtime(time.time())
    endY = end[0]
    
    for _year in range(startY, endY + 1):
        
        monthRange.append(('%d-%0.2d'%(_year, startM)))
    
    return monthRange


def Weekday(ts):
     
    return int(time.strftime('%w', time.localtime(float(ts))))

def getNow():
    return int(time.time())

def getToday():
    cur = datetime.datetime.now()
    year = cur.year
    month = cur.month
    day=cur.day
    
    return int(time.mktime(datetime.datetime(year, month, day, 0, 0, 0, 0).timetuple()))


'''
    加载 easyui模板并转换成 json格式
        
    @param typ 模板文件类型
'''
def loadEasyuiMould(typ="easyui", pt="user", retstr=False, prefix=''):
    
    view = None
    
    path = prefix + 'templates/' + pt + '/json/' + typ + '.json'
            
    if os.path.exists(path):
        try:
            fl = open(path)  
            view = fl.read()
            view = view.replace('\n','')
            view = view.replace(' ','')
            #view = json.load(fl, 'utf-8')
            
            if retstr == False:
                view = json.loads(view)
        finally:  
            fl.close()
    
    return view


'''
    加载 easyui模板并转换成 json格式
        
    @param typ 模板文件类型
'''
def loadFile(path, obj=False):
    
    view = None
            
    if os.path.exists(path):
        try:
            fl = open(path)  
            view = fl.read()
            #view = view.replace('\n','')
            #view = view.replace(' ','')
            #view = json.load(fl, 'utf-8')
            
            if obj:
                view = json.loads(view)
        finally:  
            fl.close()
    
    return view


'''
    计算函数执行时间的装饰器
        
    @param func 所要计算的执行函数
'''
def timeit(func):
    
    def wrapper(*args, **kwargs):
        
        start = time.clock()
        
        ret = func(*args, **kwargs)
        
        end = time.clock()
        
        print func.__name__, 'used:', end - start
        # logging.debug('%s used:%s'%(func.__name__, end - start))
        
        return ret
        
    return wrapper


# 标准差
def stdDeviation(a):
    l = len(a)
    m = sum(a)/l
    d = 0
    for i in a:d+=(i-m)**2
    return (d*(1/l))**0.5
    
    
def isNumber(val):
    
    if re.match(r'^(-?\d+)(\.\d+)?$', val) is not None:
        return True
    
    return False


def get_session_value(key, prefix=''):
    
    sess = web.ctx.session
    key = key + prefix
    
    return sess.get(key,  {})


def set_session_value(key, value, prefix=''):
    
    sess = web.ctx.session
    key = key + prefix
    
    sess[key] = value


def cals(v1,v2,op = 'diff',dp = 2):
    if op == 'diff':
        if v1 is not None and v2 is not None:
            return round(v1 - v2,dp)
    elif op == 'add':
        if v1 is not None or v2 is not None:
            v1 = v1 if v1 is not None else 0
            v2 = v2 if v2 is not None else 0
            return round(v1+v2,dp)
    elif op == 'div':
        if v1 and v2:
            v2 = v2* 1.0
            return round(v1/v2 *100.0,dp)

def getStrDate(y,m,d=None):
    '''
    将年月 或者年月日
    转化为格式yyyy-MM 或者yyyy-MM-dd 的字符串格式
    '''
    m = "".join(["0",str(m)]) if m<=9 else str(m)
    if d is None:
        return "".join([str(y),'-',m])
    d = "".join(["0",str(d)]) if d<=9 else str(d)
    return "".join([str(y),'-',m,'-',d])

def add_seconds(ts,count=1):
    return ts + timedelta(seconds=count).total_seconds()

def add_minutes(ts,count=1):
    return ts + timedelta(minutes=count).total_seconds()

def add_hours(ts,count=1):
    return ts + timedelta(hours=count).total_seconds()

def add_days(ts,count=1):
    return ts + timedelta(days=count).total_seconds()

def add_weeks(ts,count=1):
    return add_days(ts,count*7)

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
    
def add_years(ts,count=1):
    return add_days(ts,count*365)

def getFirstEndDayOfWeek(ts):
    cur = datetime.datetime.fromtimestamp(ts)
    
    start = int(time.mktime(datetime.datetime(cur.year, cur.month, cur.day, 0, 0, 0).timetuple()))
    start = start - 86400 * cur.weekday()
    end = start + 86400 * 6 - 1
    
    return start, end

'''
    获取给定季度的第一天和最后一天
        
'''
def getFirstEndDayOfSeason(year,season):
    sMonth = (season-1)*3+1
    eMonth = season*3
    
    d = calendar.monthrange(year, eMonth)
    
    start = int(time.mktime(datetime.datetime(year, sMonth, 1, 0, 0, 0, 0).timetuple()))
    end   = int(time.mktime(datetime.datetime(year, eMonth, d[1], 23, 59, 59, 0).timetuple()))
    
    return start, end

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
    

def is_require_time(Time, starttime=0,Interval=0,endtime=0):
        
    if Interval == 0:
        return True
    
    lt = time.localtime(Time)
    h, m, s = lt[3], lt[4], lt[5]
    
    ms = h * 3600 + m * 60 + s 
    
    if (ms- starttime) % Interval == 0:
        if endtime and endtime>0 and ms>=starttime and ms<=endtime:
            return True
        elif endtime==0 or endtime is None:
            return True
    
    return False


def data_format(datapoint=None, number=False):
    
    if not number:
        fmt = None
        datapoint = datapoint if datapoint is not None else ''
        dp = str(datapoint)
                    
        if dp and len(dp) > 0:
                        
            fmt = '%'+'.%sf'%dp
            
        return fmt
    else:
        datapoint = datapoint if datapoint is not None else ''
        dp = str(datapoint)
        
        if dp and len(dp) > 0:
            return int(dp)
        
        return None
    
def ROUND(v, dp, _round=True):
    if _round:
        return round(v, dp)
    else:
        return format_numeric(v, dp)

def format_val(v, fmt=None, number=False):
            
    if fmt is None or v == '':
        return v
    
    if number and fmt is not None and v is not None:
        return round(v, fmt)
            
    return v if v is None else (fmt %v)

def cal_addition(val1, val2, dp=None, _round=True):
    
    if isinstance(val2, list):
        for _val2 in val2:
            val1 = cal_addition(val1, _val2, dp)
        return val1
    else:
        if val1 is not None and val2 is not None:
            return (val1 + val2) if dp is None else ROUND(val1 + val2, dp, _round)
        else:
            if val1 is not None:
                return val1 if dp is None else ROUND(val1, dp, _round)
            elif val2 is not None:
                return val2 if dp is None else ROUND(val2, dp, _round)
            else:
                return None
OP_A = cal_addition

def cal_subtraction(val1, val2, dp=None, ignore=False, _round=True):

    if val1 is not None and val2 is not None:
        return (val1 - val2) if dp is None else ROUND(val1 - val2, dp, _round)
    else:
        if ignore:
            if val1 is not None:
                return val1 if dp is None else ROUND(val1, dp, _round)
            elif val2 is not None:
                return -val2 if dp is None else ROUND(-val2, dp, _round)
        return None
OP_S = cal_subtraction

def cal_multiply(val1, val2, dp=None, _round=True):
    
    if val1 is not None and val2 is not None:
        return (val1 * val2) if dp is None else ROUND(val1 * val2, dp, _round)
    return None
OP_M = cal_multiply

def cal_division(val1, val2, dp=None, _round=True):
    
    if val1 is not None and val2 is not None and val2 != 0:
        return float(val1) / val2 if dp is None else ROUND(float(val1) / val2, dp, _round)
    return None
OP_D = cal_division

def MAX(v1, v2):
    return max(v1, v2)

def MIN(v1, v2, skip_null=True):
    if skip_null:
        if v1 is None:
            return v2
        elif v2 is None:
            return v1
        else:
            return min(v1, v2)
    else:
        return min(v1, v2)
    

def cal_factor(val1, val2):
    
    if val1 is not None and val2 is not None:
        
        if isinstance(val1, basestring):
            if len(val1) == 0:
                return None
            else:
                _val1 = float(val1)
        else:
            _val1 = val1
        
        if isinstance(val2, basestring):
            if len(val2) == 0:
                return None
            else:
                _val2 = float(val2)
        else:
            _val2 = val2
        
        if _val1 != 0:
            return float(_val2 - _val1) * 100 / _val1
    
    return None

def _formatToSingleAnalysis(station):
    if not station or not station.get('Id'): return u'未知站点'
    return ("<span class='star'></span>" if station.get('Favorite', False) else "") + "<a onclick=\"window.top.ToSingle('" + station['Id'] + "', '" + station['Name'] + "','" + station['Sn'] + "');\" title='" + station['Name'] + "(" + station['Sn'] + ")' class='single-analysis-link'>" + station['Name'] + "</a>";

def _formatToSingleAnalysisFloat(station,width):
    if not station or not station.get('Id'): return u'未知站点'
    return ("<span class='star'></span>" if station.get('Favorite', False) else "") + "<div class=\"datagrid-cell-group\" style=\"width:"+str(width)+"px\"><a onclick=\"window.top.ToSingle('" + station['Id'] + "', '" + station['Name'] + "','" + station['Sn'] + "');\" title='" + station['Name'] + "(" + station['Sn'] + ")' class='single-analysis-link'>" + station['Name'] + "</a></div>";

def _formatToSingleAnalysisEvent(station):
    if not station or not station.get('Id'): return u'未知站点'
    return ("<span class='star'></span>" if station.get('Favorite', False) else "") + "<a onclick=\"window.top.ToSingleEvent(event,'" + station['Id'] + "', '" + station['Name'] + "','" + station['Sn'] + "');\" title='" + station['Name'] + "(" + station['Sn'] + ")' class='single-analysis-link'>" + station['Name'] + "</a>";

def _data_format(datapoint=None, number=False):
    
    if not number:
        fmt = None
        datapoint = datapoint if datapoint is not None else ''
        dp = str(datapoint)
                    
        if dp and len(dp) > 0:
                        
            fmt = '%'+'.%sf'%dp
            
        return fmt
    else:
        datapoint = datapoint if datapoint is not None else ''
        dp = str(datapoint)
        
        if dp and len(dp) > 0:
            return int(dp)
        
        return None

def _format(v, fmt=None, number=False):
          
    if fmt is None and v:   #默认保留1位
        return '%.1f' %v
    
    if fmt is None or v == '':
        return v
    
    if number and fmt is not None:
        return round(v, fmt)
     
    return v if v is None else (fmt %v)

def _val2unit(un, val): #"*0:开#*1:关#"
    if un == u'@ToHHMM':
        return '%02d:%02d' % (val // 100, val % 100)

    if int(val) == val: val = int(val)
    v = '*%s:'%val
    idx = un.find(v)
    if idx == -1: return val
    start = idx + len(str(v))
    un = un[start:len(un)]
    end = un.find(u'#')
    un = un[0:end]
                
    return un

def _unit2val(un, val): #"*0:开#*1:关#"
    v = ':%s#' % val
    idx = un.find(v)
    if idx == -1: return val
    un = un[0: idx]
    start = un.rfind(u'*')
    un = un[start+1: len(un)]
                
    return int(un)

def _addrisedropClass(ss, val, title=None, hidden=False, alarmstyle=True, dataclick=False, station=None, total=1, _style='default', Alarm=False): 
    
    if _style == 'sx':
        return _addrisedropClass2(ss, val, title, hidden, alarmstyle, dataclick, station, total, Alarm=Alarm)
    else:
        return _addrisedropClass1(ss, val, title, hidden, alarmstyle, dataclick, station, total, Alarm=Alarm)

def _addrisedropClass1(ss, val, title=None, hidden=False, alarmstyle=True, dataclick=False, station=None, total=1, Alarm=False): 
    
    isAlarm = False
    
    if val is None:
        span_html = '<span class="eu-alarm-val change-normal">&nbsp;</span>'
        return (span_html, isAlarm) if Alarm else span_html
    
    classStyle = 'font-normal';
    
    if ss:
        if ss['Type'] == 'cs':
            classStyle = 'timeout-gray'
            isAlarm = True
        elif ss['Ref'] is not None and ss['Count'] > 0:
            if ss['Level'] == 3 and (ss['Value'] - ss['Ref']) >= 0:
                classStyle = 'rise_red'
            elif ss['Level'] <= 2 and (ss['Value'] - ss['Ref']) >= 0:
                classStyle = 'rise_red'
            elif ss['Level'] <= 2 and (ss['Value'] - ss['Ref']) < 0:
                classStyle = 'drop_yellow'
            elif ss['Level'] == 3 and (ss['Value'] - ss['Ref']) < 0:
                classStyle = 'drop_yellow'           
            else:
                classStyle = 'yellowbg'#font-yellow
            isAlarm = True
        else:
            classStyle = 'change-normal'#'change-normal'#font-blue
        if 'Timeout-Show' in ss:
            val=ss['Timeout-Show']
            title='数据超时'
    span_html = '<span '
    if ss and dataclick: span_html += ' style="cursor:pointer;" ondblclick="DataClick(this,\'' + ss['Id'] + '\',\'' + station['Name'] + '\')"'
    span_html += ('title="' + title + '"' if title is not None else '') 
    if ss and ss.get('Timeout-Color',''): span_html +=' style="color:'+ss.get('Timeout-Color','')+'"'
    span_html += ' class="' + ('hidden ' if hidden else 'shown ') + ('eu-alarm-val ' if alarmstyle else '') + classStyle + '">' 
    span_html += (val if isinstance(val, basestring) else str(val)) + '</span>'
     
    return (span_html, isAlarm) if Alarm else span_html
    #return '<span ' + ('title="' + title + '"' if title is not None else '') + ' class="' + ('hidden ' if hidden else 'shown ') + ('eu-alarm-val ' if alarmstyle else '') + classStyle + '">' + (val if isinstance(val, basestring) else str(val)) + '</span>'

def _addrisedropClass2(ss, val, title=None, hidden=False, alarmstyle=True, dataclick=False, station=None, total=1, Alarm=False): 
    
    isAlarm = False
    
    if val is None:
        span_html = '<span class="eu-alarm-val change-normal">&nbsp;</span>'
        return (span_html, isAlarm) if Alarm else span_html    
    
    classStyle = 'font-normal';
    
    if ss:
        if ss['Type'] == 'cs':
            classStyle = 'timeout-gray'
            isAlarm = True
        elif ss['Ref'] is not None and ss['Count'] > 0:
            if ss['Level'] == 3:
                classStyle = 'alarm_lv3 '
            elif ss['Level'] == 2:
                classStyle = 'alarm_lv2 '
            else:
                classStyle = 'alarm_lv1 '
            
            if (ss['Value'] - ss['Ref']) >= 0:
                classStyle += ('alarm_up_fixed' if total > 1 else 'alarm_up')
            else:
                classStyle += ('alarm_down_fixed' if total > 1 else 'alarm_down')
            isAlarm = True
        else:
            classStyle = 'change-normal'#'change-normal'#font-blue
    
    span_html = '<span '
    if ss and dataclick: span_html += ' style="cursor:pointer;" ondblclick="DataClick(this,\'' + ss['Id'] + '\',\'' + station['Name'] + '\')"'
    span_html += ('title="' + title + '"' if title is not None else '') 
    span_html += ' class="' + ('hidden ' if hidden else 'shown ') + ('eu-alarm-val ' if alarmstyle else '') + classStyle + '">' 
    span_html += (val if isinstance(val, basestring) else str(val)) + '</span>'
     
    return (span_html, isAlarm) if Alarm else span_html
    #return '<span ' + ('title="' + title + '"' if title is not None else '') + ' class="' + ('hidden ' if hidden else 'shown ') + ('eu-alarm-val ' if alarmstyle else '') + classStyle + '">' + (val if isinstance(val, basestring) else str(val)) + '</span>'

def _create_lable_for_sensors(lst, alarmstyle=True, dataclick=False, station=None, _style='default'):
    
    if isinstance(lst, basestring): lst = [lst]
    dtyp, li = '', ''
    total = len(lst)
    for i in range(total):
        l = lst[i]
        val = l.get('val')
        ss = l.get('sensor') or {}
        title = ('%s[%s] (%s/%s)'%(ss.get('Name'), ss.get('Id'), i+1, total) if total > 1 else '%s[%s]'%(ss.get('Name'), ss.get('Id'))) if ss.get('Name') is not None and ss.get('Id') is not None else ''
        li += '<li>' + _addrisedropClass(ss, val, title, alarmstyle=alarmstyle, total=total, _style=_style) + '</li>'#, (True if i > 0 else False)
        dtyp = ss.get('DType') or ''
    
    label = '<div ' + ('class="scada6-multi-vals"' if len(lst) > 1 else '')
    if dataclick and station and dtyp in ['YL', 'SSLL', 'YuL', 'ZD', 'PH']: label += ' style="cursor:pointer;" ondblclick="DataClick(this,\'' + station['Name'] + '\',\'' + station['Id'] + '\',\'' + dtyp + '\')"'
    label += '><ul>'
    label += li
    label += '</ul></div>'
    return label

def _parse_conditions(conditions = None):

    q = {}
      
    if conditions:
        
        for c in conditions:
          
            f = c.get('Field')
            r = c.get('Relation', 'and')
            o = c.get('Operate', '')
            v = c.get('Value')
          
            if f and o:
                
                a = None
                
                if r == 'and':
                    q['$and'] = q.get('$and', {})
                    a = q['$and']
                elif r == 'or':
                    q['$or'] = q.get('$or', {})
                    a = q['$or']
                
                if a is not None:
                    if f not in a: a[f] = {}

                    if o == 'like':
                        #a.append({f:{'$regex':v}})
                        a[f]['$regex'] = v
                    elif o == '=':
                        #a.append({f:v})
                        a[f] = v
                    elif o == '>=':
                        #a.append({f:{'$gte':v}})
                        a[f]['$gte'] = v
                    elif o == '>':
                        #a.append({f:{'$gt' :v}})
                        a[f]['$gt'] = v
                    elif o == '<=':
                        #a.append({f:{'$lte':v}})
                        a[f]['$lte'] = v
                    elif o == '<':
                        #a.append({f:{'$lt' :v}})
                        a[f]['$lt'] = v
                    elif o == 'nil':
                        #a.append({f:{'$exists':False}})
                        a[f]['$exists'] = False
                    elif o == '!=':
                        #a.append({f:{'$ne':v}})
                        a[f]['$ne'] = v
                    elif o == 'in':
                        #a.append({f:{'$in':v}})
                        a[f]['$in'] = v
  
    if '$and' in q and len(q.get('$and')) == 0:
        del q['$and']
        
    if '$or' in q and len(q.get('$or')) == 0:
        del q['$or']
        
    return q

def _parse_conditions2(conditions = None, exclude=[]):
    
    q = {}
      
    if conditions:
        
        for c in conditions:
          
            f = c.get('Field')
            r = c.get('Relation', 'and')
            o = c.get('Operate', '')
            v = c.get('Value', '')
            t = c.get('DataType')
            
            if f in exclude: continue
            
            if t == 'Number' and (v is None or v == ''): 

                continue
          
            if f and o:
                
                a = None
                
                if r == 'and':
                    q['$and'] = q.get('$and', {})
                    a = q['$and']
                elif r == 'or':
                    q['$or'] = q.get('$or', {})
                    a = q['$or']
                
                if a is not None:
                  
                    if o == '=':
                        #a.append({f:v})
                        a[f] = {'op':'==', 'v':v}
                    elif o == '>=':
                        #a.append({f:{'$gte':v}})
                        a[f] = {'op':'>=', 'v':v}
                    elif o == '>':
                        #a.append({f:{'$gt' :v}})
                        a[f] = {'op':'>', 'v':v}
                    elif o == '<=':
                        #a.append({f:{'$lte':v}})
                        a[f] = {'op':'<=', 'v':v}
                    elif o == '<':
                        #a.append({f:{'$lt' :v}})
                        a[f] = {'op':'<', 'v':v}
                    elif o == '!=':
                        #a.append({f:{'$ne':v}})
                        a[f] = {'op':'!=', 'v':v}
  
    if '$and' in q and len(q.get('$and')) == 0:
        del q['$and']
        
    if '$or' in q and len(q.get('$or')) == 0:
        del q['$or']
        
    return q


#解析条件 a[f] = v改成a[f]["$eq"] = v
def _parse_conditions_1(conditions = None):
    q = {}

    if conditions:

        for c in conditions:

            f = c.get('Field')
            r = c.get('Relation', 'and')
            o = c.get('Operate', '')
            v = c.get('Value')

            if f and o:

                a = None

                if r == 'and':
                    q['$and'] = q.get('$and', {})
                    a = q['$and']
                elif r == 'or':
                    q['$or'] = q.get('$or', {})
                    a = q['$or']

                if a is not None:
                    if f not in a:
                        a[f] = {}

                    if o == 'like':
                        # a.append({f:{'$regex':v}})
                        a[f]['$regex'] = v
                    elif o == '=':
                        # a.append({f:v})
                        a[f]["$eq"] = v
                    elif o == '>=':
                        # a.append({f:{'$gte':v}})
                        a[f]['$gte'] = v
                    elif o == '>':
                        # a.append({f:{'$gt' :v}})
                        a[f]['$gt'] = v
                    elif o == '<=':
                        # a.append({f:{'$lte':v}})
                        a[f]['$lte'] = v
                    elif o == '<':
                        # a.append({f:{'$lt' :v}})
                        a[f]['$lt'] = v
                    elif o == 'nil':
                        # a.append({f:{'$exists':False}})
                        a[f]['$exists'] = False
                    elif o == '!=':
                        # a.append({f:{'$ne':v}})
                        a[f]['$ne'] = v
                    elif o == 'in':
                        # a.append({f:{'$in':v}})
                        a[f]['$in'] = v

    if '$and' in q and len(q.get('$and')) == 0:
        del q['$and']

    if '$or' in q and len(q.get('$or')) == 0:
        del q['$or']

    return q

#解析条件 与或关系为list
def _parse_conditions_3(conditions = None):

    def _addparse(a, o, f, v):
        if a is not None:
            if o == 'like':
                a.append({f: {'$regex': v}})
            elif o == '=':
                a.append({f: v})
            elif o == '>=':
                a.append({f: {'$gte': v}})
            elif o == '>':
                a.append({f: {'$gt': v}})
            elif o == '<=':
                a.append({f: {'$lte': v}})
            elif o == '<':
                a.append({f: {'$lt': v}})
            elif o == 'nil':
                a.append({f: {'$exists': False}})
            elif o == '!=':
                a.append({f: {'$ne': v}})
            elif o == 'in':
                a.append({f: {'$in': v}})

    q = {}
    if conditions:
        for c in conditions:
            f = c.get('Field')
            r = c.get('Relation', 'and')
            o = c.get('Operate', '')
            v = c.get('Value')

            if f and o:
                a = None
                if r == 'and':
                    q['$and'] = q.get('$and', [])
                    a = q['$and']
                    _addparse(a, o, f, v)
                elif r == 'or':
                    q['$or'] = q.get('$or', [])
                    a = q['$or']
                    _addparse(a, o, f, v)

    return q

#过滤条件 与或关系为list
def _parse_conditions_4(conditions = None, exclude = []):

    def _addparse(a, o, f, v):
        if a is not None:

            if o == '=':
                a.append({f: {'op': '==', 'v': v}})
            elif o == '>=':
                a.append({f: {'op': '>=', 'v': v}})
            elif o == '>':
                a.append({f: {'op': '>', 'v': v}})
            elif o == '<=':
                a.append({f: {'op': '<=', 'v': v}})
            elif o == '<':
                a.append({f: {'op': '<', 'v': v}})
            elif o == '!=':
                a.append({f: {'op': '!=', 'v': v}})
            elif o == 'nil':
                a.append({f: {'op': 'nil', 'v': v}})

    q = {}

    if conditions:
        for c in conditions:
            f = c.get('Field')
            r = c.get('Relation', 'and')
            o = c.get('Operate', '')
            v = c.get('Value', '')
            t = c.get('DataType')

            if f in exclude:
                continue

            # if t == 'Number' and (v is None or v == ''):
            #     continue

            if f and o:
                a = None
                if r == 'and':
                    q['$and'] = q.get('$and', [])
                    a = q['$and']
                    _addparse(a, o, f, v)
                elif r == 'or':
                    q['$or'] = q.get('$or', [])
                    a = q['$or']
                    _addparse(a, o, f, v)

    if '$and' in q and len(q.get('$and')) == 0:
        del q['$and']

    if '$or' in q and len(q.get('$or')) == 0:
        del q['$or']

    return q

''' 1:开关量  |2:模拟量 | 3:累计量 '''
TYPE_KAIGULIANG = '1'
TYPE_MONILIANG  = '2'
TYPE_LEIJILIANG = '3'


'''
    根据传感器信息得到列头标题
'''
def _getColTitleBySensor(ss, waterreport=False, prefix = ""):
    
    unit = ss.get('Unit')
    title = ss.get('Name')
    stype = str(ss.get('VType', '') or '')
    
    if stype == TYPE_KAIGULIANG:
        #title = '%s(%s)'%(title, u'次')
        title = '%s'%(title)
    elif stype == TYPE_LEIJILIANG:
        if not waterreport:
            title = '%s(%s)'%(title,unit) if unit and len(unit) > 0 else title
        else:
            title = u'%s<br/>用量(%s)'%(title,unit) if unit and len(unit) > 0 else title
        title = prefix + title
    else:
        title = '%s(%s)'%(title,unit) if unit and len(unit) > 0 else title
        
    return title


def _isRequireTime(Time, starttime=0,Interval=0,endtime=0):
        
        if Interval == 0:
            return True
        
        lt = time.localtime(Time)
        h, m, s = lt[3], lt[4], lt[5]
        
        ms = h * 3600 + m * 60 + s 
        
        if (ms- starttime) % Interval == 0:
            if endtime and endtime>0 and ms>=starttime and ms<=endtime:
                return True
            elif endtime==0 or endtime is None:
                return True
        
        return False

        
def _time_format(v, fmt=None):
    
    if v is None or v == '':
        return v
    
    v = int(v)
    
    if v == 0:
        return u'0分'
     
    day = v / (24 * 3600) 
 
    hour = (v - day * 24 * 3600) / 3600 
    
    mins = (v - day * 24 * 3600 - hour * 3600) / 60
    
    sec = v - day * 24 * 3600 - hour * 3600 - mins * 60

    ret = ''
    if day >0:
        ret += '%s天'%day
    if hour >0:
        ret += '%s小时'%hour
    if mins > 0:
        ret += '%.0f分'%mins
    if sec > 0:
        ret += '%.0f秒'%sec
    
    return ret


def format_numeric(v, dp = 0):
    if v is None or dp is None:
        return v
    return int(v * (10 ** dp)) * 1.0 / (10 ** dp)


def format_positions(pos, latFirst=False):
    
    ret = []
    
    if not pos: return ret
    
    position = pos.split(',') or ['']
    if len(position) == 2:
        if latFirst: ret = [float(position[1]), float(position[0])]
        else: ret = [float(position[0]), float(position[1])]
    
    return ret


def transfer_row_column(data, frozen_field='dt', column2row=True):
    
    def row_define(kwArgs):
        
        return {
            'datatype':kwArgs.get('datatype', 'number'),
            'field':kwArgs.get('field'),
            'title':kwArgs.get('title'),
            'align':kwArgs.get('align', 'center'),
            'colspan':kwArgs.get('align', 1),
            'hidden':kwArgs.get('align', False),
            'rowspan':kwArgs.get('rowspan', 1),
            'width':kwArgs.get('width', 100)
        }
    
    
    #fcols = data.get('frozenColumns') or [[]]
    cols = data.get('columns') or [[]]
    rows = data.get('rows') or []
    
    rownum = len(cols)
    if rownum == 0:
        return
    
    standard = [[] for _ in range(rownum)]
    
    colnum = 0
    for c in cols[0]:
        if not c.get('hidden'):
            colnum += c.get('colspan') or 1
            
    for cn in range(colnum):
        for rn in range(rownum):
            standard[rn].append(None)
    
    for rn in range(rownum):
        cn = 0
        for c in cols[rn]:
            if not c.get('hidden'):
                colspan = c.get('colspan') or 1
                for i in range(colspan):
                    if i == 0:
                        while cn<len(standard[rn]) and standard[rn][cn] is not None:#盐城汇津水务SCADA6.0分区计量报表功能修改三列表头跨行问题修复
                            cn=cn+1
                        standard[rn][cn] = c
                    cn += 1
                
                rowspan = c.get('rowspan') or 1
                for i in range(1, rowspan):
                    _rn = rn + i
                    _cn = cn - colspan
                    standard[_rn][_cn]={} #盐城汇津水务SCADA6.0分区计量报表功能修改三列表头跨行问题修复
                    # for sc in cols[_rn][_cn:]:
                    #     if not sc.get('hidden'):
                    #         _colspan = sc.get('colspan') or 1
                    #         for i in range(_colspan):
                    #             if i == 0: # and sc.get('field')
                    #                 standard[_rn][_cn] = sc
                    #             _cn += 1
    
    frozenColumns = [[]]
    columns = [[]]
    lst = [{} for _ in range(colnum)]
    
    field_idxs = {}
    for cn in range(colnum):
        for rn in range(rownum):
            std = standard[rn][cn]
            if std is not None:
                if std.get('field'):
                    field_idxs[std.get('field')] = cn #start from 0
                lst[cn]['col_%s'%rn] = std.get('title')
    
    frozenColumns[0].append(row_define({'field':'num', 'title':u'序号', 'width':60}))
    for i in range(rownum):
        frozenColumns[0].append(row_define({'field':'col_%s'%i, 'title':'', 'width':100 if i == 2 else 120}))
    
    for idx in range(len(rows)):
        row = rows[idx]
        field = str(idx)
        columns[0].append(row_define({'field':field, 'title':row.get(frozen_field)}))
        for k, v in row.items():
            rn = field_idxs.get(k)
            if rn is not None:
                lst[rn][field] = v
    
    for idx in range(len(lst)):
        lst[idx]['num'] = idx + 1
                
    
    data['frozenColumns'] = frozenColumns
    data['columns'] = columns
    data['rows'] = lst
    #data['total'] = len(lst)

def datetime_offset_by_month(datetime1, n = 1):
 
    # create a shortcut object for one day
    one_day = datetime.timedelta(days = 1)
 
    # first use div and mod to determine year cycle
    q,r = divmod(datetime1.month + n, 12)
 
    # create a datetime2
    # to be the last day of the target month
    datetime2 = datetime.datetime(
        datetime1.year + q, r + 1, 1) - one_day
 
    '''
       if input date is the last day of this month
       then the output date should also be the last
       day of the target month, although the day
       www.iplaypython.com
       may be different.
       for example:
       datetime1 = 8.31
       datetime2 = 9.30
    '''
 
    if datetime1.month != (datetime1 + one_day).month:
        return datetime2
 
    '''
        if datetime1 day is bigger than last day of
        target month, then, use datetime2
        for example:
        datetime1 = 10.31
        datetime2 = 11.30
    '''
 
    if datetime1.day >= datetime2.day:
        return datetime2
 
    '''
     then, here, we just replace datetime2's day
     with the same of datetime1, that's ok.
    '''
 
    return datetime2.replace(day = datetime1.day)

    
def ts_date(t):
    
    return int(time.mktime(datetime.date.fromtimestamp(t).timetuple()))


import service

def gen_event_code(obj, size=5):
    
    cid  = obj.get('cid')
    typo = obj.get('type')
    
    if not cid or not typo:
        return {'type':typo, 'code':''}
    
    code = None
    
    if typo not in ['ts', 'cx', 'gd']:
        typo = 'gd'
    
    sequence = service.biz.sequences.get({'cid':cid})
                    
    if sequence is None or typo not in sequence:
        typoseq = {'idx':0, 'perfix':None}
        if typo == 'ts': typoseq['perfix'] = 'T'
        elif typo == 'cx': typoseq['perfix'] = 'C'
        #elif typo == 'gd': typoseq['perfix'] = 'W'
        else: typoseq['perfix'] = 'W'
    else:
        typoseq = sequence.get(typo)
        
    fmt = None
    if typo == 'gd':  
        gdlb = service.biz.uddics.get({'cid':cid, 'Code':'GDLB'}) or {}
        rlst = gdlb.get('Records', [])
        if len(rlst) > 0: fmt = rlst[0].get('extend') if rlst[0].get('extend') else fmt
        
    if fmt: #自定义工单格式
        dtfmt = {'YYYYMMDD':'%Y%m%d', 'YYYYMM':'%Y%m', 'YYYY':'%Y'}
        p = re.compile(r'{.*?\}')
        arr = p.findall(fmt)
        fmt1, fmt2 = arr[0].replace('{','').replace('}',''), arr[1].replace('{','').replace('}','')
        dt = YMD(time.time(), dtfmt.get(fmt1, '%Y'))
        size = len(fmt2) if fmt2 else size
        
        typoseq['idx'] = typoseq.get('idx') + 1
        if typoseq.get('code'):
            _dt = typoseq.get('code')[1:len(typoseq.get('code')) - size]
            if _dt != dt: typoseq['idx'] = 1
        
        code = ('%s%s%.' + str(size) + 'd')%(typoseq['perfix'], dt, typoseq['idx'])
    else:
        year = Y(time.time())
        typoseq['idx'] = typoseq.get('idx') + 1
        if typoseq.get('code'):
            _year = typoseq.get('code')[1:5]
            if _year != year: typoseq['idx'] = 1
        
        if typo == 'gd':
            code = '%s%s%.5d'%(typoseq['perfix'], year, typoseq['idx'])
        else:
            code = '%s%s%.4d'%(typoseq['perfix'], year, typoseq['idx'])
    
    return {'type':typo, 'code':code, 'size':size}


def get_event_no_size(obj, size=5):
    
    cid  = obj.get('cid')
    typo = obj.get('type')
    
    if typo not in ['ts', 'cx', 'gd']:
        typo = 'gd'
    
    fmt = None
    if typo == 'gd':  
        gdlb = service.biz.uddics.get({'cid':cid, 'Code':'GDLB'}) or {}
        rlst = gdlb.get('Records', [])
        if len(rlst) > 0: fmt = rlst[0].get('extend') if rlst[0].get('extend') else fmt
        
    if fmt: #自定义工单格式
        p = re.compile(r'{.*?\}')
        arr = p.findall(fmt)
        fmt2 = arr[1].replace('{','').replace('}','')
        size = len(fmt2) if fmt2 else size
        
    return size


def reset_event_code(obj, size=5):
    
    def __event_code(_typoseq, _fmt, _size):
        
        if _fmt: #自定义工单格式
            dtfmt = {'YYYYMMDD':'%Y%m%d', 'YYYYMM':'%Y%m', 'YYYY':'%Y'}
            p = re.compile(r'{.*?\}')
            arr = p.findall(_fmt)
            fmt1, fmt2 = arr[0].replace('{','').replace('}',''), arr[1].replace('{','').replace('}','')
            dt = YMD(time.time(), dtfmt.get(fmt1, '%Y'))
            _size = len(fmt2) if fmt2 else _size
            
            _typoseq['idx'] = _typoseq.get('idx') + 1
            if _typoseq.get('code'):
                _dt = _typoseq.get('code')[1:len(_typoseq.get('code')) - _size]
                if _dt != dt: _typoseq['idx'] = 1
            
            code = ('%s%s%.' + str(_size) + 'd')%(_typoseq['perfix'], dt, _typoseq['idx'])
        else:
            year = Y(time.time())
            _typoseq['idx'] = _typoseq.get('idx') + 1
            if _typoseq.get('code'):
                _year = _typoseq.get('code')[1:_size]
                if _year != year: _typoseq['idx'] = 1
            
            if typo == 'gd':
                code = '%s%s%.5d'%(_typoseq['perfix'], year, _typoseq['idx'])
            else:
                code = '%s%s%.4d'%(_typoseq['perfix'], year, _typoseq['idx'])
        
        _typoseq['code'] = code
        query = {'gdbh':code} if typo == 'gd' else {'sq_bh':code}
        if service.biz.events.exists(query):
            return __event_code(_typoseq, _fmt, _size)
        else:
            #_typoseq['idx'] += 1
            return _typoseq
            
    
    cid  = obj.get('cid')
    typo = obj.get('type')
    
    if not cid or not typo:
        return {'type':typo, 'code':''}
    
    if typo not in ['ts', 'cx', 'gd']:
        typo = 'gd'
    
    sequence = service.biz.sequences.get({'cid':cid}) or {'_id':str(ObjectId())}
                    
    if sequence is None or typo not in sequence:
        typoseq = {'idx':0, 'perfix':None}
        if typo == 'ts': typoseq['perfix'] = 'T'
        elif typo == 'cx': typoseq['perfix'] = 'C'
        #elif typo == 'gd': typoseq['perfix'] = 'W'
        else: typoseq['perfix'] = 'W'
    else:
        typoseq = sequence.get(typo)
        
    fmt = None
    if typo == 'gd':  
        gdlb = service.biz.uddics.get({'cid':cid, 'Code':'GDLB'}) or {}
        rlst = gdlb.get('Records', [])
        if len(rlst) > 0: fmt = rlst[0].get('extend') if rlst[0].get('extend') else fmt
        
    typoseq = __event_code(typoseq, fmt, size)
            
    service.biz.sequences.upsert(sequence['_id'], ** {'cid':cid, typo:typoseq})
            
    return {'type':typo, 'code':typoseq['code'], 'size':size}


def get_object_value(obj, f):
    
    def __get(__obj, __farr):
        if len(__farr) > 1:
            return __get(__obj.get(__farr.pop()) or {}, __farr)
        return __obj.get(__farr.pop())
    
    farr = f.split('.')
    farr.reverse()
    return __get(obj, farr) if len(farr) > 0 else None

def dateDiffInSeconds(date1, date2):
    timedelta = date2 - date1
    return timedelta.days*24*3600 + timedelta.seconds


#判断是否内网IP
def is_internal_ip(ip):
    def ip_into_int(_ip):
        # 先把 192.168.1.13 变成16进制的 c0.a8.01.0d ，再去了“.”后转成10进制的 3232235789 即可。
        # (((((192 * 256) + 168) * 256) + 1) * 256) + 13
        return reduce(lambda x,y:(x<<8)+y,map(int,_ip.split('.')))
    if ip=='127.0.0.1':return True
    ip = ip_into_int(ip)
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    return ip >> 24 == net_a or ip >>20 == net_b or ip >> 16 == net_c


# 求最大公约数
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# 求最小公倍数
def lcm(a, b):
    return a * b / gcd(a, b)


def handleExcelRow(data, column_map, bindings={}, fetch_binding_name=False):
    '''按配置处理单行数据
    @param data: 读取到的原始行数据
    @param column_map: 根据列标题筛选的配置信息
    @param bindings: 字典字段配置
    @param fetch_binding_name: 字典字段是否获取名称
    '''
    def getFromDict(binding, k):
        if k in binding:
            return binding[k]
        elif str(k) in binding:
            return binding[str(k)]
        return None
    
    def parseNumber(v):
        '''浮点型整数转为整型'''
        return int(v) if v % 1 == 0 else v
    
    def parseString(v):
        if isinstance(v, basestring):
            return v.strip()
        elif isinstance(v, float):
            return str(parseNumber(v))
        else:
            return str(v)

    row = {}
    empty_fields = []
    for i, v in enumerate(data):
        if i in column_map:
            config = column_map[i] # 当前列配置
            field = config['Field']
            if not v and v != 0:
                if config.get('Default') is not None: # 默认值
                    row[field] = config['Default']
                    if config['DataType'] == 'String' and config.get('ShowType') == 'combo' and fetch_binding_name:
                        # combo字段
                        row[field + 'nm'] = getFromDict(bindings.get(config['Ext'], {}), row[field])
                if row.get(field) is None and config.get('Required'):
                    # 必填项未填写
                    empty_fields.append(field)
            else:
                if config['DataType'] == 'String':
                    _v = parseString(v)

                    if config.get('ShowType') == 'combo':
                        row[field] = None
                        bind = bindings.get(config['Ext'], {})
                        for k, text in bind.items():
                            if _v == text:
                                row[field] = k
                                if fetch_binding_name:
                                    row[field + 'nm'] = text
                                break
                        if row[field] is None and config.get('Default') is not None:
                            # 如果填的值不存在数据字典中，取默认值
                            row[field] = config['Default']
                            if fetch_binding_name:
                                row[field + 'nm'] = bind.get(config['Default'])
                    else:
                        row[field] = _v

                elif config['DataType'] == 'Number':
                    try:
                        if config.get('ShowType') == 'combo':
                            _v = parseString(v)

                            row[field] = None
                            bind = bindings.get(config['Ext'], {})
                            for k, text in bind.items():
                                if _v == text:
                                    row[field] = parseNumber(float(k))
                                    if fetch_binding_name:
                                        row[field + 'nm'] = text
                                    break
                            if row[field] is None and config.get('Default') is not None:
                                # 如果填的值不存在数据字典中，取默认值
                                row[field] = config['Default']
                                if fetch_binding_name:
                                    row[field + 'nm'] = bind.get(config['Default'])
                        else:
                            row[field] = parseNumber(float(v))
                    except:
                        row[field] = None
                elif config['DataType'] == 'Date':
                    try:
                        fmt = config.get('Ext') or '%Y-%m-%d'
                        if isinstance(v, float):
                            from xlrd import xldate_as_tuple
                            dt = xldate_as_tuple(v, 0)
                            row[field] = YMD(time.mktime(
                                (dt[0], dt[1], dt[2], dt[3], dt[4], dt[5], 0, 0, 0)), fmt)
                        else:
                            dt = re.findall(r'\d+', v)
                            if len(dt) > 0:
                                li = [1, 1, 1, 0, 0, 0, 0, 0, 0]
                                for i in range(len(dt)):
                                    li[i] = int(dt[i])
                                row[field] = YMD(time.mktime(tuple(li)), fmt)
                            else:
                                row[field] = None
                    except:
                        row[field] = None
                else:
                    row[field] = v

                if row[field] is None and config.get('Required'):
                    # 针对有填写值，但不符要求的必填项
                    empty_fields.append(field)
    return row, empty_fields



if __name__ == "__main__":
    
    #getMonthRange('2014-01', '2014-01')
    #print getDayCount(y=2004,m=2)
    #print getTCompareMonth('2012-11')
    
    #print getStartEndOfThisPeriod()
    
    '''def _cal_factor(val1, val2):
        
        if val1 is not None and len(val1) > 0 and val2 is not None and len(val2) > 0:
            _val1 = float(val1)
            _val2 = float(val2)
            
            if _val1 != 0:
                return float(_val2 - _val1) * 100 / _val1
        
        return None
    
    print _cal_factor('1199.0', '788.0')'''
    
    #v = OP_A(None,[2,3,None,5,6])
    #print v
    s, e = float(YMD2TS('2016-03-28')), float(YMD2TS('2016-03-31'))
    s, e = getLastMonthSamePeriod(s, e)
    print YMD(s), YMD(e)
    
