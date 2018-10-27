# -*- coding: UTF-8 -*-
# Module  : py
# Description :获取数据
# Author  : Wujj
# Date    : 2017-11-4
# Version : 1.0


from ui import path, CRUD, wildcard
from web.contrib.template import render_mako
import customs.stock.service.tushare_proapi  as tushare_proapi



@path("/stock/report/test.json")
class StockReportTest(POST):
    def get_data(self, AType=None, _scid=None, _role=None, _user=None, _cid=None, _customer=None, *args, **kwArgs):



    def action(self, dks=None, *args, **kwArgs):
        return self.get_data(*args, **kwArgs)