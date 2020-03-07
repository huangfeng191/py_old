# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/3/2
# Version : 1.0


from method import *
from  customs.tide.service import utils as tide_utils
from customs.tide.service.bean.base import *
from customs.tide.service.bean.out import *
class EmphasisTake:
    '''
    获取数据
        take
            type
            config
    '''
    def __init__(self,take):
        self.take=take
        self.type=take.get("type")

    def get(self):
        config=self.take.get(self.type)
        take=self.take
        ret=None
        if self.type=="table":
            # 未了能正确取 jump 数据
            c=queryTideTableParse(config,take)

            ret=rule_doing_table(c,None)
            if config.get("fields"):
                pass

            return  ret
                # config=config.get("fields")
        elif self.type=="log":
            bean=eval("tide_%s_log"%config.get("hook"))
            fetchKey=tide_utils.compressObject({"fetch.key":take.get("key")})
            o=bean.get(fetchKey)
            if o.get("data"):
                ret ={}
                for s in config.get("fields"):
                    ret[s]=o["data"].get(s)
        return ret


def doTideLog(hook, data):
    if hook != "cell":

        fetchKey = tide_utils.compressObject({"fetch.key": data.get("fetch").get("key")})
        bean=eval("tide_%s_log" % hook)
        old=bean.get(fetchKey)
        if old:
            old.update(data)
            data=old
        eval("tide_%s_log" % hook).upsert(**data)

def deleteTideLog(hook,key):
    fetchKey = tide_utils.compressObject({"fetch.key": key})
    eval("tide_%s_log" % hook).delete(fetchKey,multi=True)


def deleteTideTable(nm,key):
    k = tide_utils.compressObject({"key": key})
    level=key.get("level")
    eval("%s_%s"%(nm,level)).delete( k, multi=True)

def saveTideTable(nm,key,data,carousel):
    data.update({"key":key})
    if carousel:
        data.update({"carousel":carousel})
    level=key.get("level")
    eval("%s_%s"%(nm,level)).upsert( **data)


def queryTideTableParse (config,take):
    c = {}
    c.update(config)
    if "query" not in c:
        c["query"] = {}
    fetchKey = tide_utils.compressObject({"key": take.get("key")})
    c["query"].update(fetchKey)
    c["nm"] = "%s_%s" % (c["nm"], take.get("key").get("level"))
    return c

