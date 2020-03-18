# -*- coding: UTF-8 -*-
# Module  : py
# Description :基本接口
# Author  : Wujj
# Date    : 2017-11-5
# Version : 1.0



import ctx
from copy import deepcopy
from service import comm
import math

from customs.stock.service.basic import *

from customs.stock.service.tushare_beans import *

# 考虑用on_upsert
#stock_basics.inject(industry_classified,"i_c","code",False,"code")

import json
import time
from misc import utils
import tushare as ts
ts.set_token(ctx.tushreToken)

# table_nm 就是接口名
def getInterfaceData(table_nm="stock_basic",fields=None,**kwargs):
    pro=None
    i=1
    while True:
       try:
        pro = ts.pro_api()
        break
       except:
           time.sleep(60*i)
           i=i+1
           pro = ts.pro_api()
           print ("Reconnecting...")
    try:
        data=pro.query(table_nm,fields,**kwargs )
    except:
        print "I`am error "
        time.sleep(60 * i)
        data = pro.query(table_nm, fields, **kwargs)
    return data
# 将数据保存到数据库
def handleDate(table_nm,fields,config,**kws):

    df = getInterfaceData(table_nm=table_nm, fields=fields, **kws)
    # df_index = df.index
    # 暂时不用
    key_query={}
    key_last=""
    if config.get("indexKey"):
        for r in config.get("indexKey").split(","):
            key_query[r]=None
            key_last=r

    if not isinstance(df, list):
        l = json.loads(df.to_json(orient='records'))
        for i, r in enumerate(l):
            # 从对象中获取primary
            k_query= dict(filter(lambda o: o[0] in key_query.keys(), r.items()))
            r_one=eval(table_nm).get(k_query)
            if r_one:
                r=dict(r_one,**deepcopy(r))
            eval(table_nm).upsert(**r)
            # ---------------------------------------------
            # 数组对象插入配置
            if("2" in config.get("storage_way",[]) or[] ):
                # 支持插入多个表
                for storage_config in config.get("storage_config","").split("\n"):
                    if storage_config.split(",")>1:
                        storage_table_nm=storage_config.split(",")[0]
                        storage_table_psn=storage_config.split(",")[1]
                        InjectArray(r,storage_table_nm,{storage_table_psn:r.get(storage_table_psn)},k_query,key_last,config)
def InjectArray(r,storage_table_nm=None,storage_table_psn={},query={},sort="",config={},**kwargs):
    table_nm=config.get("table_nm")
    one=eval(storage_table_nm).get(storage_table_psn)
    if one:
        if not one.get(table_nm,[]):
            one[table_nm]=[]
        target_arr=one.get(table_nm,[])
        isNew=True
        for one_r in target_arr:
            if utils.dict_compare(one_r,query):
                one_r.update(r)
                isNew=False
        if isNew:
            target_arr.append(r)        
        if sort:
            target_arr.sort(key=lambda x:x.get(sort))
            one[table_nm+"2o"]=target_arr[-1]
        eval(storage_table_nm).upsert(**one)
    else:
        pass


# 配置参数 ,只解析一次参数
def rulePart(params,send_params={}):
    # variable 可变参数，会影响请求次数
    # normal 替换常量参数
    # must 一般常量参数
    analysis_o={"variable":[],"normal":[],"must":{}}
    must=analysis_o["must"]
    variable=analysis_o["variable"]
    normal=analysis_o["normal"]
    for k, r2 in params.items():
        pass
        if (isinstance(r2, dict)):
            if r2.get("type") == "loop":
                # basic 接口表里的字段
                # type:loop basic 接口表字段   from 其他表字段  from_k 其他表字段主键
                # 此处可以添加参数，
                one_com={"basic": k, "type": r2.get("type"), "from": r2.get("from"), "from_k": r2.get("from_k"), "from_q": r2.get("from_q"),"combo":r2.get("combo",1)}
                variable.append(one_com)
            elif r2.get("type") == "date":
                # type：date  basic 接口表字段   from_k  从哪个字段获取， send_params 从那个字段获取的条件
                # last 暂时不支持，
                one_com = {"basic": k, "type": r2.get("type"),"operate":r2.get("operate","="),"from_k":r2.get("from_k"),"param2o":{}  }
                if  send_params.get(one_com.get("from_k")):
                    if one_com.get("operate","=")=="=":
                        one_com["param2o"]={k:send_params.get(one_com.get("from_k"))}
                    else:
                        one_com["param2o"]={k:{"$"+one_com.get("operate") :send_params.get(one_com.get("from_k")) }}
                    normal.append(one_com)
        else:
            must[k] = r2
    for r in normal:
        for k2,r2 in r.get("param2o").items():
            must[k2]=r2
            pass
        pass        
    return analysis_o
def ruleCombine(variable=[],normal=[],must={},ret=[]):
    if not variable:
       ret.append(must)
    for r_c in variable:    
        if r_c.get("type") == "loop":
            l = eval(r_c.get("from")).items(query=r_c.get("from_q"), fields=[r_c.get("from_k")], _sort=[(r_c.get("from_k"), 1)])
            combo=r_c.get("combo")
            if combo==1:
                for r_l in l:
                    must[r_c.get("basic")] = r_l.get(r_c.get("from_k"))
                    ret.append(deepcopy(must))
            else:
                k=[]
                l=list(l)
                for i in range(0,len(l)):
                    r_l=l[i]
                    if ((i+1)%combo ==0) or (i== len(l)-1) :
                        k.append(r_l.get(r_c.get("from_k")))
                        must[r_c.get("basic")] = ",".join(k)
                        ret.append(deepcopy(must))
                        k=[]
                    else:
                        k.append(r_l.get(r_c.get("from_k")))

            pass



                    # send_params 暂未实现
# 返回的数组是需要调用多少次接口
def analysisParams(configRow,config_params,send_params=None,**kwargs) :
    params=None
    # 此处可以扩展
    if config_params:
        if config_params.get("sendWay")=="increase":
            params=configRow.get("param2")
        else:
            params = configRow.get("param")


    a_params = json.loads(params)
    ret = []
    for r in a_params:
        analysis_o= rulePart(r,send_params)
        ruleCombine(ret=ret,**analysis_o)
    return ret

# send_param 是在 admin 页面上设置的，
def getProInfo(table_nm,logId,config_param={},send_param={},**kwargs):

    if table_nm:
        log=pro_interface_log.get(logId)
        configRow=pro_interface_config.get({"table_nm":table_nm})
        if configRow:
            pro_interface_log.upsert(**{"_id":log.get("_id"),"config":configRow})
        fields = []
        for r in configRow.get("colInp").split("\n"):
            ar = r.split(",")
            if ar[0]:
                fields.append(ar[0])

        limit = {
            "type": "minute",
            "times": 0,
            "time": time.time()
        }

        # 方法参数  目的是接口可能有参数要求，写成了一个数组，可循环调用接口
        if configRow.get("param"):
            params=analysisParams(configRow,config_param,send_param)
            i_count=len(params)
            i_step=0


            log["i_count"]=i_count
            log["i_step"]=0
            log["state"]=1
            pro_interface_log.upsert(**log)
            for r in params:
                handleDate(table_nm,fields,configRow,**r)
                i_step+=1
                if i_step % (int(i_count/100) or 1)==0 :
                  print "总共%d,完成%d,time:%d"%(i_count,i_step,time.time()-limit["time"])
                  if r:
                      r=json.dumps(r)
                  pro_interface_log.upsert(**{"_id": logId, "i_step": i_step,"last_param":r})

                limit["times"] += 1;
                if (ctx.tushreMinuteLimit and limit["times"] > ctx.tushreMinuteLimit):

                    delay=None
                    if(limit.get("type")=="minute"):
                        delay = math.ceil(60-time.time() + limit["time"])
                        if delay>0:
                            print "sleep:%d"%delay
                            time.sleep(delay)
                    limit["time"]= time.time()
                    limit["times"] = 0

            pro_interface_log.upsert(**{"_id":logId,"state":2,"i_step":i_step,"last_param":"","continued": round((int(time.time())-log.get("created"))/60)})
        else:    
            handleDate(table_nm,fields,configRow)
            pro_interface_log.upsert(**{"_id": logId, "state": 2, "i_step": 1,"continued": round((int(time.time())-log.get("created"))/60)})

    return "OK"
