# -*- coding: UTF-8 -*-
# Module  : py
# Description :获取数据
# Author  : Wujj
# Date    : 2017-11-4
# Version : 1.0


from ui import path, CRUD, wildcard

from customs.stock.service.report  import *

from webservice import POST, GET

@path("/stock/report/test.json")
class StockReportTest(POST):
    def get_data(self,method_tp, *args, **kwArgs):
        if method_tp:
            ret=eval(method_tp)(**kwArgs)
            return ret
        pass



    def action(self, dks=None, *args, **kwArgs):
        return self.get_data(*args, **kwArgs)