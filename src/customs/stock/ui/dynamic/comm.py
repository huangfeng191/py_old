# -*- coding: UTF-8 -*-
# Module  : py
# Description :测试接口
# Author  : Wujj
# Date    : 2019/09/01
# Version : 1.0
from webservice import POST
from ui import  path,wildcard,CRUD
from customs.stock.service.dynamic.comm import *

from customs.stock.service.dynamic.rule import *
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
          else:
              return CRUD.action(self, act, *args, **kwArgs)

    def test(self, _id=None, *args, **kwArgs):
        one=self.module.get(_id)
        del one["_id"]
        dynamic_comm_test_log.upsert(**one)
        return eval(one.get("method"))(**(one.get("params")or {}))

