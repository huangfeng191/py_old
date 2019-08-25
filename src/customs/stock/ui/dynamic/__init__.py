# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2019/08/24
# Version : 1.0


from ui import path, CRUD, wildcard,ArrayCRUD
import web
from web.contrib.template import render_mako
render_dynamic= render_mako(directories=["customs/stock/templates/pro/dynamic", "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")

from customs.stock.service.dynamic import *

@path("/dynamic/step.html")
class DynamicStep:
    def GET(self, _cid = None, *args, **kwargs):
        return render_dynamic["step"]()
        
@wildcard("/dynamic/step/")
class DynamicStepCRUD(CRUD):
    def __init__(self):
        self.module = dynamic_step
        
        
@path("/dynamic/link.html") 
class DynamicLink:
    def GET(self, _cid = None, *args, **kwargs):
        return render_dynamic["link"]()
        
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