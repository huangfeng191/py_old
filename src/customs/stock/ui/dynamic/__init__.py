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

from customs.stock.service.dynamic import *

from customs.stock.ui.dynamic.comm import *

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
        else:
            return ArrayCRUD.action(self, act, *args, **kwArgs)

  def test(self, _id=None,pid=None, *args, **kwArgs):
      p=self.module.get(pid)
      one=None
      for r in p.get("cell"):
          if r.get("_id")==_id:
              one=r
      loadRule(**one)
      return "OK"

@bind_outGenerate
def loadRule(**kwArgs):
  ruleType=kwArgs.get("ruleType")
  if ruleType=="last": # 可以将方法也配置成参数
      getLastResult(**kwArgs)

