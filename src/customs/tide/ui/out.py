# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/3/11
# Version : 1.0

from ui import wildcard,CRUD,path
from  customs.tide.service.bean.out  import *

from web.contrib.template import render_mako
tide_out= render_mako(directories=["customs/tide/templates/", "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")

from  customs.tide.service.bean.base  import *

from customs.tide.service.expose.expose import *



@path("/tide/out/record.html")
class TideOutRecord:
    def GET(self, _cid = None, *args, **kwargs):
        return tide_out["out/record"]()





@wildcard("/tide/out/record/")
class TideOutRecordCRUD(CRUD):
    def __init__(self):
        self.module = tide_chains_log
    def action(self, act, *args, **kwArgs):
          if act == 'getOpts':
              return self.getOpts(*args, **kwArgs)
          else:
              return CRUD.action(self, act, *args, **kwArgs)

    def getOpts(self, record=None, *args, **kwArgs):



        ret=None
        log = self.module.get(record.get("logId"))

        for c in log.get("chains"):
            Hook = c.get(record["hook"])
            if Hook.get("hookId") == record["hookId"]:
                T = TideCellOthers("cell",c["cell"].get("hookId"))
                ret=T.geTabletOpts( Hook.get("take").get("table")["nm"],Hook.get("take").get("key"))
        return {
            "rows":[ret]
        }
    def query(self, count=True, *args, **kwArgs):
        conditions = kwArgs.get('conditions', [])
        del kwArgs["conditions"]
        query = tide_utils.parse_conditions_CRUD(conditions).get('$and', {})
        o={}
        for r in ["logId","hook","hookId"]:
            o[r]=query[r]
            del query[r]
        log=self.module.get(o.get("logId"))
        cs=[]
        total=0
        for c in log.get("chains"):
            Hook=c.get(o["hook"])
            if Hook.get("hookId")==o["hookId"]:
                kwArgs["query"]=query
                kwArgs["query"]["key"]=Hook.get("take").get("key")
                kwArgs["query"]=compressObject(kwArgs["query"])
                table=Hook["take"].get("table")
                cs = eval("%s_%s"%(table["nm"],table["hook"])).items(*args, **kwArgs)
                total=cs.count()
                break
        return {
            'total':total,
            'rows': list(cs)
        }


