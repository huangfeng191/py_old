# -*- coding: utf-8 -*-
# Module  : ctx
# Author  : fengfeng
# Date    : 2017-7-15
# Version : 1.0


import os
from pymongo.mongo_client import MongoClient
# 默认时区为GMT+8
ZONE = +8

#获取config配置文件
if __file__:  #当前文件

    __Configured = False
    __CfgFile = os.path.dirname(__file__) + "/config/config.json"
    __Cfg = {}
def config():

    global __Configured,__CfgFile,__Cfg

    if not __Configured:
        if os.path.exists(__CfgFile):
            with open(__CfgFile,'r') as fd:
                __Cfg = eval(fd.read(),{'__builtins__':None}) or {}
        __Configured=True
    return __Cfg


def get(ns,key,default_value=None):

    r = config().get(ns,None)
    return (r and r.get(key,default_value)) or default_value


# 数据库前缀
DB_PREFIX = get("sys","db_prefix","")

#数据库
mdb = MongoClient(maxPoolSize=get("sys","maxPoolSize", 128), connect=False, ** get("sys","mongodb")) # Mongodb数据库

def get_db(module):

  return mdb[DB_PREFIX + module]

# Endless loop!
while True:

    try:
        print 'connect MongoDB......'
        mdb["test"]["__test__"].count()
        print 'Pass.'
        break
    except KeyboardInterrupt:
        print ("Terminated!")
        break
    except:
        print ("Unable to connect " + str(get("sys","mongodb")))
        print ("Reconnecting...")

db_source = {'default':mdb}

# 配置数据库
cmdb = get_db("config")
# stock数据库
stockdb = get_db("mystock")
rabbitdb = get_db("rabbit")
# 结点前缀
ND_PREFIX = get("sys","node_prefix","")

#导入客户系统
customs = get("sys", "customs", [])

tltoken=get("tonglian", "token", [])


# 上面是mongodb