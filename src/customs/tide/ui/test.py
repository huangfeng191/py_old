# -*- coding: UTF-8 -*-
# Module  : py
# Description :测试
# Author  : Wujj
# Date    : 2020/2/3
# Version : 1.0

from ui import wildcard,CRUD,path


from web.contrib.template import render_mako
render_tide= render_mako(directories=["customs/tide/templates/", "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")

from  customs.tide.service.bean.misc import *

import logging
import importlib

from customs.tide.service.dual.rule.test import *
from customs.tide.service.gather.layer import *
from customs.tide.service.gather.test import *
from customs.tide.service.utils.test import *
from customs.tide.service.expose.test import *
#  测试写的写的方法
@path("/tide/test/method.html")
class TideTest:
    def GET(self, _cid = None, *args, **kwargs):
        return render_tide["test/method"]()

@wildcard("/tide/test/method/")
class TideTestCRUD(CRUD):

    def __init__(self):
        self.module = tide_test
        
    def action(self, act, *args, **kwArgs):   
      if act == 'doing':
          return self.doing(*args, **kwArgs)
      else:
          return CRUD.action(self, act, *args, **kwArgs)
              
    def doing(self, row=None, *args, **kwArgs):
        if row:
            if row.get("path") and row.get("method"):
                try:
                    # importlib.import_module("%s" % row.get("path"))
                    # importlib.import_module("customs.tide.service.gather")
                    doing={"doing":"%s(%s)"%(row.get("method"),row.get("args",""))}
                    row.update(doing)
                    tide_test_log.upsert(**row)
                    eval(doing.get("doing"))
                except Exception, e:
                    logging.error(e)
                    raise Exception(e)

        return []