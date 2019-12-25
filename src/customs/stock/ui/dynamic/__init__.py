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
from misc.utils import _parse_conditions








@path("/dynamic/step.html")
class DynamicStep:
    def GET(self, _cid = None, *args, **kwargs):
        return render_dynamic["step"]()
        
@wildcard("/dynamic/step/")
class DynamicStepCRUD(CRUD):
    def __init__(self):
        self.module = dynamic_step
    def action(self, act, *args, **kwArgs):
          if act == 'generateStep':
              return self.generateStep(*args, **kwArgs)
          else:
              return CRUD.action(self, act, *args, **kwArgs)

    def generateStep(self, *args, **kwArgs):

       return doStepOne(**kwArgs)


    # st = time.time()
    # log = doLinkOne(**{"linkId": _id})
    # log["continue"] = (time.time() - st)
    # dynamic_link_log.upsert(**log)
    # return log



@wildcard("/dynamic/step/link/")
class DynamicStepLink(ArrayCRUD):
  def __init__(self):
    self.module = dynamic_step
    self.array = 'link'
  def action(self, act, *args, **kwArgs):
        if act == 'query':
            conditions = kwArgs.get('conditions', [])
            query = _parse_conditions(conditions).get('$and', {})
            if query.get("ck")==1:
                kwArgs["conditions"]=[{ "Field": "__pid", "Operate": "=", "Value": query.get("__pid"), "Relation": "and" }]

                return ArrayCRUD.action(self, act, *args, **kwArgs)
            else:
                return self.queryAll(*args, **kwArgs)
        elif act=="bindLink":
            return self.bindLink(*args, **kwArgs)
        else:
            return ArrayCRUD.action(self, act, *args, **kwArgs)



        return self.action("insert",record=one)
  def bindLink(self,links,pid):
      step = self.module.get(pid)
      if step:
          step[self.array]=[]
      step[self.array]=links
      self.module.upsert(**step)

      return "OK"


  def queryAll(self, record=None, *args, **kwArgs):
      conditions = kwArgs.get('conditions', [])
      query = _parse_conditions(conditions).get('$and', {})
      step=self.module.get(query.get("__pid"))
      o_links={}
      for r in step.get("link", []):
          o_links[r.get("_id")]=r
      links_keys=o_links.keys();
      del kwArgs["conditions"]
      ret=dynamic_link.items(**kwArgs)
      res=list(ret)
      if ret:
          for r in  res:
             if(r.get("_id") in links_keys):
                 r.update({"ck":1,"generateW":o_links.get(r.get("_id")).get("generateW")})
      return {'total': ret.count(), 'rows': res}






# 设置 cell
        
@wildcard("/dynamic/link/")
class DynamicLinkCRUD(CRUD):

    def __init__(self):
        self.module = dynamic_link
    def action(self, act, *args, **kwArgs):
          if act == 'generateLink':
              return self.generateLink(*args, **kwArgs)
          if act == 'copy':
              return self.copy(*args, **kwArgs)
          else:
              return CRUD.action(self, act, *args, **kwArgs)

    def copy(self, fromId=None, **kwArgs):

        one = self.module.get(fromId)
        del one["_id"]

        return self.action("insert", record=one)
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
        elif act == 'copyToOther':
            return self.copyToOther(*args, **kwArgs)
        else:
            return ArrayCRUD.action(self, act, *args, **kwArgs)
  # 将配置复制到 本选中的 link 下
  def copyToOther(self,from_id=None,fromPid=None,toPid=None,**kwArgs):

        p = self.module.get(fromPid)
        record={"__pid":toPid}
        if "cell" not in p:
            p["cell"]=[]
        for r in p.get("cell",[]):
            if r.get("_id")==from_id:
                record.update(r)
                record["_id"]=str(ObjectId())


        return self.action("insert",record=record)
  # 测试单个 cell
  def test(self, _id=None, *args, **kwArgs):
      p=self.module.get(kwArgs.get("__pid"))
      one=None
      tier={
          "linkId":p.get("_id"),
          "cellId":_id
      }
      for r in p.get("cell"):
          if r.get("_id")==_id:
              one=r

      one["logSource"]="dynamic_link_cell_log"
      loadRule(tier,**one)
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
        saveWithOutClear(out, one)
        return self.module.delete(**one)

    def __init__(self):
        self.module = dynamic_link_cell_log