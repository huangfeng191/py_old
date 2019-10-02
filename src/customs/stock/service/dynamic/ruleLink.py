# -*- coding: UTF-8 -*-
# Module  : py
# Description :用规则调用的方法
# Author  : Wujj
# Date    : 2019/09/25
# Version : 1.0


from customs.stock.service.dynamic.ruleFun import *


@wrapper.calc_runtime_wrapper
def doLinkOne(linkId,**kwargs):
    pass
    # 此处记录日志
    # 告知输出从哪里去取以及 如何取
    link,noGenerate=getLinkLog(linkId)
    if not noGenerate:
        link["cell"]=sorted(link["cell"],lambda x:x.w)
        for one in link.get("cell",[]):
            one["logSource"] = "dynamic_link_cell_log"
            rule_data=loadRule(**one)
            one["log"]=rule_data.get("log")
            link["output_log"]=one["log"]
        return dynamic_link_log.upsert(**link)
    else:
        return link


def getLinkLog(linkId):
    link = dynamic_link.get(linkId)
    noGenerate=False
    if (link.get("frequency")):
        outFrequency = reuse.getFrequencyStart(link.get("frequency"))
        link["outFrequency"] = outFrequency
        link["link_id"] = link["_id"]
        old = dynamic_link_log.get({"link_id": link["_id"], "outFrequency": outFrequency, "sn": link.get("sn")})
        if old:
            if link.get("outGenerate") == "first":
                noGenerate=True
            link["_id"] = old.get("_id")
        else:
            del link["_id"]
    return link,noGenerate
# 获取时没生成 先获取
def getStepResult(linkId,**kwArgs):
    log,noGenerate=getLinkLog(linkId)
    if not noGenerate:
        doLinkOne(linkId)

    pass

