# -*- coding: utf-8 -*-
# Module  :
# Author  : fengfeng
# Date    : 2018-07-25
# Version : 1.0

from ui import path, wildcard, CRUD,web
from service.biz import user,customer,ddics
import web
import json
from misc import utils


import customs.stock.service.basic as basic

from web.contrib.template import render_mako
render_out = render_mako(directories=[ "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")


@path("/ctx.js")
class Ctx:


    def GET(self, _customer=None, _cid=None, _role=None, *args, **kwArgs):

        web.header("Content-Type", "text/javascript", True)
        # user=utils.get_session_value('user')
        u=user.get({"acc":"sandy"})
        c = customer.get({"code": "stock"})
        GCtx={}

        GCtx["user"]=u
        GCtx["customer"]=c
        return "var GCtx = %s; " % json.dumps(GCtx)



@path("/prostock/bindings.js")
class ProStockBindings:


    def GET(self, _customer=None, _cid=None, _role=None, *args, **kwArgs):

      web.header("Content-Type", "text/javascript", True)

      #用户自定义数据字典
      bindings, codeset = [], set([])

      for dd in ddics.items(size=99999):
          if dd.get('Code', '') not in codeset:
              bindings.append(dd)


      for r in basic.pro_interface_config.items(query={'cid':_cid}):
          if   'code' in r:
              for rr in r.get("dtls"):
                  rr["name"]=r.get("nrssm")
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
      aRelation=[]

      for r in ddics.items(query={"Relation":{'$ne':""}}):
          aRelation.append({"_id":r.get("Relation"),"name":r.get("Name"),"value":r.get("Code")})
      bindings.append(
        {"Code":"Relation","Records":aRelation}
      )     
      return "var GBindings = %s; " % json.dumps(bindings)



@path("/out/index.html")
class OutIndex:
    def GET(self, _cid = None, *args, **kwargs):
        return render_out["webpack/out"]()

@path("/inner/index.html")
class InnerIndex:
    def GET(self, _cid = None, *args, **kwargs):
        return render_out["webpack/index"]()


