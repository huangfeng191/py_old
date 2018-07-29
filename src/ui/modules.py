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
import urllib



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


# 动态导入模块
import importlib

for o in ctx.customs:

    try:
        importlib.import_module("customs.%s.ui" % o)
    except Exception, e:
        logging.error(e)



# html 格式导出
@path("/export")
class DataExport:
    def POST(self):

        params = web.input(exportContent=None, FileName=None)

        web.header('Content-Type', 'application/vnd.ms-excel')
        # web.header('Transfer-Encoding','chunked')
        fn = urllib.unquote(params["FileName"].encode("UTF-8"))

        if 'MSIE' in web.ctx.environ['HTTP_USER_AGENT']:
            fn = fn.decode('UTF-8').encode('GBK')
        elif 'rv:1' in web.ctx.environ['HTTP_USER_AGENT']:
            fn = fn.decode('UTF-8').encode('GBK')

        web.header('Content-Disposition', 'attachment;filename=' + fn)

        return "<html><head><meta http-equiv='content-type' content='application/ms-excel; charset=UTF-8'/></head><body>" + \
               params["exportContent"] + "</body></html>"
