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




@path("/tide/log/chain.html")
class TideLogChain:
    def GET(self, _cid = None, *args, **kwargs):
        return tide_log["log/chain"]()

@wildcard("/tide/log/chain/")
class TideLogCRUD(CRUD):
    def __init__(self):
        self.module = tide_chains_log
    def action(self, act, *args, **kwArgs):
          if act == 'query':
              return self.query(*args, **kwArgs)
          else:
              return CRUD.action(self, act, *args, **kwArgs)

    def query(self, record=None, *args, **kwArgs):

            conditions = kwArgs.get('conditions', [])
            query = tide_utils.parse_conditions_CRUD(conditions).get('$and', {})
            log=self.module.get(query.get("_id"))
            Log=Tide_log_info(log.get("topHookId"),log.get("topHook"),log.get("_id"))

            res=Log.getLayers(query.get("hook"),query.get("pid","")) or []


            return {'total': len(res), 'rows': res}

@path("/tide/log/chains.html")
class TideLogChains:
    def GET(self, _cid = None, *args, **kwargs):
        return tide_log["log/chains"]()




@wildcard("/tide/log/chains/")
class TideLogChainsCRUD(CRUD):
    def __init__(self):
        self.module = tide_chains_log
        def action(self, act, *args, **kwArgs):
          if act == 'query':
              return self.query(*args, **kwArgs)
          else:
              return CRUD.action(self, act, *args, **kwArgs)



    def query(self, count=True, *args, **kwArgs):

        res = CRUD.query(self, count=count, *args, **kwArgs)

        return res