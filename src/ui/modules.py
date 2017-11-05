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
from web.contrib.template import render_mako


# render_jsb = render_mako(directories=['templates/jsb','templates/page/jsb','templates/biz','templates'], input_encoding='utf-8', output_encoding='utf-8',)
render_jsb = render_mako(directories=['test'], input_encoding='utf-8', output_encoding='utf-8',)

# 跳转根目录
@path("/")
class Index:
    def __init__(self):
        self.index = ctx.get("web", "index", "/stock/admin.html")

    def GET(self, _cid=None, _customer=None, _role=None, *args, **kwArgs):
        index = self.index
        raise web.seeother(index)


@path("/stock/index.html")
class StockIndex:
    def GET(self, _cid=None, *args, **kwargs):
        return "Hello world!"
@path("/stock/index1.html")
class StockIndex1:
    def GET(self, _cid=None, *args, **kwargs):
        print 1
        return render_jsb["temp"]()

@path("/stock/index2.html")
class StockIndex2:
    def GET(self, _cid=None, *args, **kwargs):
        print 1
        return render_jsb.temp()

# 动态导入模块
import importlib

for o in ctx.customs:

    try:
        importlib.import_module("customs.%s.ui" % o)
    except Exception, e:
        logging.error(e)
