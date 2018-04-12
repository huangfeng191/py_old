# -*- coding: utf-8 -*-
# datetime是Python处理日期和时间的标准库。
import datetime
import time
dNow=datetime.datetime.now() 
# datetime.now()返回当前日期和时间，其类型是datetime。
print dNow
print dNow.day
print u"dNow.day=时间:%s"%(dNow.day) 
print u"dNow.weekday()= 时间:%s"%(dNow.weekday()) 

# 获取第几天
print dNow.strftime('%j')

d1=datetime.datetime(2017,1,1)
print d1.strftime('%j')