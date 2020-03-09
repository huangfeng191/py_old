# -*- coding: UTF-8 -*-
# Module  : py
# Description :log
# Author  : Wujj
# Date    : 2020/3/9
# Version : 1.0

from ui import wildcard,CRUD,path

from web.contrib.template import render_mako
tide_log= render_mako(directories=["customs/tide/templates/", "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")
from  customs.tide.service.bean.base  import *

from customs.tide.service.expose.expose import *

@path("/tide/log/plan.html")
class TideLogPlan:
    def GET(self, _cid = None, *args, **kwargs):
        return tide_log["log/plan"]()



@wildcard("/tide/log/plan/")
class TideLogPlanCRUD(CRUD):

    def __init__(self):
        self.module = tide_plan_log

@wildcard("/tide/log/measure/")
class TideLogMeasureCRUD(CRUD):
    def __init__(self):
        self.module = tide_measure_log


@wildcard("/tide/log/step/")
class TideLogStepCRUD(CRUD):
    def __init__(self):
        self.module = tide_step_log

@wildcard("/tide/log/link/")
class TideLogLinkCRUD(CRUD):
    def __init__(self):
        self.module = tide_link_log

@wildcard("/tide/log/cell/")
class TideLogCellCRUD(CRUD):
    def __init__(self):
        self.module = tide_cell_log