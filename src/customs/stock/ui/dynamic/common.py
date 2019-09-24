# -*- coding: UTF-8 -*-
# Module  : py
# Description :测试接口
# Author  : Wujj
# Date    : 2019/09/01
# Version : 1.0
import json
from webservice import POST

from ui import  path,wildcard,CRUD
from customs.stock.service.dynamic.common import *

from customs.stock.service.dynamic.rule import *
from customs.stock.service.dynamic.ruleFun import *
from customs.stock.service.dynamic.ruleLink import *
from web.contrib.template import render_mako
dynamic_comm= render_mako(directories=["customs/stock/templates/pro/dynamic/comm", "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")


@path("/dynamic/comm/test.html")
class DynamicCommTest:
    def GET(self, _cid = None, *args, **kwargs):
        return dynamic_comm["test"]()


@wildcard("/dynamic/comm/test/")
class DynamicCommTestCRUD(CRUD):
    def __init__(self):
        self.module = dynamic_comm_test
    def action(self, act, *args, **kwArgs):
          if act == 'test':
              return self.test(*args, **kwArgs)
          elif act == 'copy':
              return self.copy(*args, **kwArgs)
          else:
              return CRUD.action(self, act, *args, **kwArgs)

    def copy(self,_id=None):
        one = self.module.get(_id)
        del one["_id"]
        return self.module.upsert(**one)
    def test(self, _id=None, frequency=None,*args, **kwArgs):
        logSource="dynamic_comm_test_log"
        one=self.module.get(_id)
        one["tid"] = one["_id"]
        del one["_id"]
        if(frequency):
            outFrequency=reuse.getFrequencyStart(frequency)
            one["outFrequency"]=outFrequency
            old=eval(logSource).get({"tid":one["tid"],"outFrequency":outFrequency,"sn":one.get("sn")})
            if old:
                if one.get("outGenerate")=="first":
                    return "OK"
                one["_id"]=old.get("_id")
        log=eval(logSource).upsert(**one)

        p=json.loads(one.get("args") )# 方法参数
        if one.get("params"):
            p["params"]=json.loads(one.get("params")) # 公用参数
        p["log"]=log
        p["logSource"]=logSource
        return eval(one.get("method"))(**p)


@wildcard("/dynamic/comm/test/log/")
class DanamicCommCRUD(CRUD):
    def __init__(self):
        self.module = dynamic_comm_test_log

    def action(self, act, *args, **kwArgs):
          if act == 'multiDelete':
              return self.multiDelete(*args, **kwArgs)
          else:
              return CRUD.action(self, act, *args, **kwArgs)

    def multiDelete(self, ids=None, *args, **kwArgs):
        return dynamic_comm_test_log.delete({"_id":{'$in':ids}},**{"multi":True})
