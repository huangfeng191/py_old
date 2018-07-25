
from ui import path, wildcard, CRUD,web
from customs.stock.service import *
import web
import json
from misc import utils
@path("/ctx.js")
class JsbDids:


    def GET(self, _customer=None, _cid=None, _role=None, *args, **kwArgs):

        web.header("Content-Type", "text/javascript", True)
        user=utils.get_session_value('user')
        GCtx={}

        GCtx["user"]=user
        return "var GCtx = %s; " % json.dumps(GCtx)



@path("/bindings.js")
class Bindings:


    def GET(self, _customer=None, _cid=None, _role=None, *args, **kwArgs):

      web.header("Content-Type", "text/javascript", True)

      #用户自定义数据字典
      bindings, codeset = [], set([])
      for r in stock_interface_config.items(query={'cid':_cid}):
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
