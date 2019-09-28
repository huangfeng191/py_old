# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2019/08/24
# Version : 1.0

from ui import ArrayCRUD,path,wildcard,CRUD
import web
from web.contrib.template import render_mako
render_dynamic= render_mako(directories=["customs/stock/templates/pro/dynamic", "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")

from customs.stock.service.dynamic import dynamic_link_cell_log,dynamic_link

from customs.stock.ui.dynamic.common import *
from bson.objectid import ObjectId
import json









@path("/dynamic/step.html")
class DynamicStep:
    def GET(self, _cid = None, *args, **kwargs):
        return render_dynamic["step"]()
        
@wildcard("/dynamic/step/")
class DynamicStepCRUD(CRUD):
    def __init__(self):
        self.module = dynamic_step
        



# 设置 cell
        
@wildcard("/dynamic/link/")
class DynamicLinkCRUD(CRUD):

    def __init__(self):
        self.module = dynamic_link
    def action(self, act, *args, **kwArgs):
          if act == 'generateLink':
              return self.generateLink(*args, **kwArgs)
          else:
              return CRUD.action(self, act, *args, **kwArgs)

    def generateLink(self, _id,*args, **kwArgs):
       st=time.time()
       log=doLinkOne(**{"linkId":_id})
       log["continue"]=(time.time()-st)
       dynamic_link_log.upsert(**log)
       return log


@path("/dynamic/link/cell.html") 
class dynamicLinkCell:
    def GET(self, _cid = None, *args, **kwargs):
        return render_dynamic["cell"]()
        

@wildcard("/dynamic/link/cell/")
class DynamicLink(ArrayCRUD):
  def __init__(self):
    self.module = dynamic_link
    self.array = 'cell'

  def action(self, act, *args, **kwArgs):
        if act == 'test':
            return self.test(*args, **kwArgs)
        elif act == 'copy':
            return self.copy(*args, **kwArgs)
        else:
            return ArrayCRUD.action(self, act, *args, **kwArgs)

  def copy(self,_id=None,**kwArgs):

        p = self.module.get(kwArgs.get("__pid"))
        record={"__pid":kwArgs.get("__pid")}
        for r in p.get("cell",[]):
            if r.get("_id")==_id:
                record.update(r)
                record["_id"]=str(ObjectId())


        return self.action("insert",record=record)
  def test(self, _id=None,pid=None, *args, **kwArgs):
      p=self.module.get(pid)
      one=None
      for r in p.get("cell"):
          if r.get("_id")==_id:
              one=r
      one["logSource"]="dynamic_link_cell_log"
      loadRule(**one)
      return "OK"




@path("/dynamic/link/cell/log.html")
class DynamicLinkCellLog:
    def GET(self, _cid = None, *args, **kwargs):
        return render_dynamic["cell_log"]()

@wildcard("/dynamic/link/cell/log/")
class DynamicLinkCellLogCRUD(CRUD):
    def action(self, act, *args, **kwArgs):
          if act == 'delete':
              return self.delete(act,*args, **kwArgs)
          else:
              return CRUD.action(self, act, *args, **kwArgs)

    def delete(self, act,  *args, **kwArgs):

        one = self.module.get(kwArgs.get("record").get("_id"))
        out = json.loads(one.get("out"))
        dealWithOutClear(out, one)
        return self.module.delete(**one)

    def __init__(self):
        self.module = dynamic_link_cell_log