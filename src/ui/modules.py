# -*- coding: utf-8 -*-
# Module  : ui.modules
# Author  : fengfeng
# Date    : 2017-07-15
# Version : 1.0

# 导入path 处理
import logging
from ui import path
import ctx
import web


# 跳转根目录
@path("/")
class Index:
    def __init__(self):
        self.index = ctx.get("web", "index", "/stock/index.html?tp=1")

    def GET(self, _cid=None, _customer=None, _role=None, *args, **kwArgs):
        index = self.index
        raise web.seeother(index)


@path("/stock/index.html")
class StockIndex:
    def GET(self, _cid=None, *args, **kwargs):
        return "Hello world!"


# 动态导入模块
import importlib

for o in ctx.customs:

    try:
        importlib.import_module("customs.%s.ui" % o)
    except Exception, e:
        logging.error(e)
