# -*- coding: UTF-8 -*-
# Description 查询数据
from ui import path, CRUD, wildcard
import web
from web.contrib.template import render_mako
from customs.stock.service.tushare_proapi import *
render_pro_stock = render_mako(directories=["customs/stock/templates/pro", "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")



from customs.stock.service.tushare_proapi import *

def bindinterfaceConfig(func):
    def _bindinterfaceConfig(self,act, *args, **kwArgs):
        params = web.input(table_nm='')
        if( act in ["query","insert","update","delete","importData"]) and params.get("table_nm"):
          # self.module=eval(params.get("table_nm"))
          self.module=eval(params.get("table_nm"))
          return func(self,act, *args, **kwArgs)
        return func(self,act, *args, **kwArgs)
    return _bindinterfaceConfig

@path("/prostock/interfaceconfig.html")
class ProStockInterfaceconfig:
    def GET(self, _cid=None, *args, **kwargs):
        return render_pro_stock["interfaceconfig"]()


@wildcard("/prostock/interfaceconfig/")
class ProStockInterfaceconfigCRUD(CRUD):
    def __init__(self):
        self.module = pro_interface_config
    def query(self, count=True, *args, **kwArgs):

       res = CRUD.query(self, count=count, *args, **kwArgs)

       return res



@path("/prostock/interfacedata.html")
class ProStockInterfaceData:
    def GET(self, _cid = None, *args, **kwargs):
        return render_pro_stock["interfaceData"]()


@wildcard("/prostock/interfacedata/")
class ProStockInterfaceDataCRUD(CRUD):

    def __init__(self):
        self.module = pro_interface_config
    @bindinterfaceConfig
    def action(self, act, *args, **kwArgs):
         return CRUD.action(self, act, *args, **kwArgs)




@path("/prostock/bindings.js")
class ProStockBindings:


    def GET(self, _customer=None, _cid=None, _role=None, *args, **kwArgs):

      web.header("Content-Type", "text/javascript", True)

      #用户自定义数据字典
      bindings, codeset = [], set([])
      for r in pro_interface_config.items(query={'cid':_cid}):
          if   'code' in r:
              for rr in r.get("dtls"):
                  rr["name"]=r.get("nm")
                  rr["value"]=r.get("code")
              bindings.append(
        {"Code":r.get("code"),"Records":r.get("dtls",[])}
      )
      bindings.append(
        {"Code":"STATE","Records":[
          {"_id":"1","name":"启用", "value":"1"},
          {"_id":"2","name":"停用", "value":"2"},
        ]}
      )
      return "var GBindings = %s; " % json.dumps(bindings)
