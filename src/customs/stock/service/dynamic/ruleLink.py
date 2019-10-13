# -*- coding: UTF-8 -*-
# Module  : py
# Description :用规则调用的方法
# Author  : Wujj
# Date    : 2019/09/25
# Version : 1.0


from customs.stock.service.dynamic.ruleFun import *


# 1 计算每一个 cell
# 2 将结果日志记录到 dynamic_link_log 的 field:output_log
@wrapper.calc_runtime_wrapper(" do one link ")
def doLinkOne(linkId,**kwargs):
    pass
    # 此处记录日志
    # 告知输出从哪里去取以及 如何取
    link,noGenerate=getLinkLog(linkId)
    if not noGenerate:
        link["cell"]=sorted(link["cell"],key=lambda x:x["w"])

        for one in link.get("cell",[]):
            one["logSource"] = "dynamic_link_cell_log"
            rule_data=loadRule(**one)
            # one["log"]=rule_data.get("log")
            if "log" in rule_data:
              link["output_log"]=rule_data.get("log")
        return dynamic_link_log.upsert(**link)
    else:
        return link


def getLinkLog(linkId):
    link,noGenerate=getDynamicLog(linkId,"dynamic_link","link_id")
    return link,noGenerate



# 获取时没生成 先获取
def getStepResult(linkId,**kwArgs):
    log,noGenerate=getLinkLog(linkId)
    if not noGenerate:
        doLinkOne(**{"linkId":linkId})

    pass

def getStepLog(stepId):
    link,noGenerate=getDynamicLog(stepId,"dynamic_step","step_id")
    return link,noGenerate


# 1 计算每一个 link
# 2 将结果日志记录到 dynamic_step_log 的 field:output_log
@wrapper.calc_runtime_wrapper(" do step one ")
def doStepOne(**kwargs):
    stepId=kwargs["stepId"]
    pass

    step_log,noGenerate=getStepLog(stepId)
    if not noGenerate:
        st=time.time()
        step_log["link"]=sorted(step_log["link"],key=lambda x:x.get("generateW"))
        for one in step_log.get("link",[]):
            link_log=doLinkOne(**{"linkId":one["_id"]})
            step_log["output_log"]=link_log # 将最后一个处理的 link 结果写入 step 的 output_log 表示此step 的最后输出
        step_log["continue"] = (time.time() - st)
        return dynamic_step_log.upsert(**step_log)
    else:
        return step_log




# Todo: 可以改成通用的方法
#  outFrequency
#  noGenerate
#  sn
#
def getDynamicLog(source_id,source,log_key):
    source_log = eval(source).get(source_id)
    noGenerate=False
    if (source_log.get("frequency")):
        outFrequency = reuse.getFrequencyStart(source_log.get("frequency"))
        source_log["outFrequency"] = outFrequency
        source_log[log_key] = source_log["_id"]
        old =eval(source+"_log").get({log_key: source_log["_id"], "outFrequency": outFrequency, "sn": source_log.get("sn")})
        if old:
            if source_log.get("outGenerate") == "first":
                noGenerate=True
            source_log["_id"] = old.get("_id")
        else:
            del source_log["_id"]
    return source_log,noGenerate


