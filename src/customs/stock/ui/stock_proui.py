# -*- coding: UTF-8 -*-
# Description 查询数据
from ui import path, CRUD, wildcard
import web
from web.contrib.template import render_mako
render_pro_stock = render_mako(directories=["customs/stock/templates/pro", "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")

import json

import customs.stock.service.basic as basic
from customs.stock.service.tushare_proapi  import *
import service.biz


@path("/prostock/interfaceconfig.html")
class ProStockInterfaceconfig:
    def GET(self, _cid=None, *args, **kwargs):
        return render_pro_stock["interfaceconfig"]()


@wildcard("/prostock/interfaceconfig/")
class ProStockInterfaceconfigCRUD(CRUD):
    def __init__(self):
        self.module = basic.pro_interface_config
    def query(self, count=True, *args, **kwArgs):

       res = CRUD.query(self, count=count, *args, **kwArgs)

       return res


@path("/prostock/interfacelog.html")
class ProstockInterfacelog:
    def GET(self, _cid = None, *args, **kwargs):
        return render_pro_stock["interfacelog"]()
        
@wildcard("/prostock/interfacelog/")
class ProstockInterfacelogCRUD(CRUD):

    def __init__(self):
        self.module = pro_interface_log


@path("/prostock/interfacedata.html")
class ProStockInterfaceData:
    def GET(self, _cid = None, *args, **kwargs):
        return render_pro_stock["interfaceData"]()



def bindinterfaceConfig(func):
    def _bindinterfaceConfig(self,act, *args, **kwArgs):
        params = web.input(table_nm='')
        if( act in ["query","insert","update","delete","importData"]) and params.get("table_nm"):
          # self.module=eval(params.get("table_nm"))
          self.module=eval(params.get("table_nm"))
          return func(self,act, *args, **kwArgs)
        return func(self,act, *args, **kwArgs)
    return _bindinterfaceConfig


@wildcard("/prostock/interfacedata/")
class ProStockInterfaceDataCRUD(CRUD):

    def __init__(self):
        self.module = basic.pro_interface_config
    @bindinterfaceConfig
    def action(self, act, *args, **kwArgs):
         return CRUD.action(self, act, *args, **kwArgs)







@path("/prostock/admin.html")
class StockAdmin:
    def GET(self, _cid=None, *args, **kwargs):
        return render_pro_stock["admin"]()


@wildcard("/prostock/admin/")
class StockAdminCRUD(CRUD):
    def __init__(self):
        self.module = basic.pro_admin_save
    def action(self, act, *args, **kwArgs):
        if act == 'getInfo':
            return self.getProInfo(*args, **kwArgs)
        if act == 'getInfoNormal':
            return self.getInfoNormal(*args, **kwArgs)

        return CRUD.action(self, act, *args, **kwArgs)
    #config_param 接口参数
    # send_param  自定义接口参数
    def getProInfo(self, table_nm=None,config_param={},send_param={}, *args, **kwArgs):
        log=pro_interface_log.upsert(**{"table_nm":table_nm,"send_param":send_param,"config_param":config_param,"i_count":1,"state":0,"tp":"get_data"})
        getProInfo(table_nm,logId=log.get("_id"),config_param=config_param,send_param=send_param)
        print table_nm+"end"
        return "OK"
    def getInfoNormal(self, table_nm=None,config_param={},send_param={}, *args, **kwArgs):
        log=pro_interface_log.upsert(**{"table_nm":table_nm,"send_param":send_param,"config_param":config_param,"i_count":1,"state":0,"tp":"get_data"})
        getProInfo(table_nm,logId=log.get("_id"),config_param=config_param,send_param=send_param)
        print table_nm+"end"
        return "OK"


@path("/prostock/multiconfig.html")
class Prostockmulticonfig:
    def GET(self, _cid = None, *args, **kwargs):
        return render_pro_stock["multiconfig"]()

@wildcard("/prostock/multiconfig/")
class ProstockmulticonfigCRUD(CRUD):

    def __init__(self):
        self.module = pro_multi_data

    def action(self, act, *args, **kwArgs):
          if act == 'basetree':
              return self.basetree(*args, **kwArgs)
          elif act == 'getConfigs':
              return self.getConfigs(*args, **kwArgs)
          else:
              return CRUD.action(self, act, *args, **kwArgs)
    def getConfigs(self,query):
        old=self.module.get({"sn":query.get("multi_sn")})
        old["colInp"]=[]
        o={"rows":[old]}
        if old.get("select_config",[]):
            a_select=old.get("select_config",[])
            for r in a_select:
                if r.get("checked"):
                    cols=filter(lambda x:x.get("checked"),r.get("cols",[]))
                    pre=""
                    config_row=pro_interface_config.get({"table_nm":r.get("id")})
                    if config_row:
                        if r.get("id") != old.get("basic"):
                            if(config_row.get("storage_way") in["2"]): # 数组方式
                                pre=r.get("id") +"2o."
                            else:
                                pre = r.get("id") + "."
                        config_row_a=config_row.get("colInp").split("\n")
                        config_row_o={}
                        for row_a2 in config_row_a:
                            config_row_o[row_a2.split(",")[0]]=pre+row_a2
                        for r2 in cols:
                            if r2.get("id") in config_row_o:
                                old["colInp"].append(config_row_o.get(r2.get("id")))
        old["colInp"]="\n".join(old["colInp"])
        return o
    def getLastInfo(self,sid):
        old=self.module.get(sid)
        o={}
        if old.get("select_config",[]):
            pass
            a_select=old.get("select_config",[])
            for r in a_select:
                o[r.get("id")]={"id":r.get("id"),"checked":r.get("checked")}
                o[r.get("id")]["cols"] = {}
                for r2 in r.get("cols"):
                    o[r.get("id")]["cols"][r2.get("id")]=r2
        return o
    def basetree(self, record=None,sid=None, *args, **kwArgs):
        l=basic.pro_interface_config.items(_sort=[("w",1)])
        ret=[]
        for r in l:
            ret.append(r)
            r["id"] = r.get("table_nm")
            r["nm"] = r["nm"] +"+"+ r.get("table_nm")
            # r["checked"]=1
            old_one=self.getLastInfo(sid).get(r["id"]) if sid else  {}
            old_one_cols={}
            if old_one:
                old_one_cols = old_one.get("cols") or{}
                r["checked"]=old_one.get("checked") or 0
            for i,row in enumerate(r.get("colInp").split("\n")):
                spans=row.split(",")
                col={"nm":spans[2]+"+"+spans[0],"pId":r.get("table_nm"),"id":spans[0],"w": None}
                if old_one_cols.get(col.get("id")):
                    col["w"]=old_one_cols.get(col.get("id")).get("w")
                    col["checked"]=old_one_cols.get(col.get("id")).get("checked") or 0
                ret.append(col)
        ret.sort(key=lambda x: x.get("w") if x.get("w") else 999)

        return ret

@path("/prostock/dlginterfacedata.html")
class ProstockDlginterfacedata:
    def GET(self, _cid = None, *args, **kwargs):
        return render_pro_stock["dlginterfacedata"]()
