# -*- coding: UTF-8 -*-
# Module  : py
# Description :测试
# Author  : Wujj
# Date    : 2020/2/17
# Version : 1.0
from factor import *
from customs.tide.service.bean.base import *
from customs.stock.service.tushare_beans import *
from tache import *
def test_QueryParsed():
    '''
        解析query 配置参数 , 支持 condition 与  key : value 方式
    Returns:

    '''

    # query, layer
    Q=QueryParsed({
                "cal_date": {
                    "type": "date",
                    "restrain":"cycle", #
                    "operate": "<="
                },

                "is_open":1


            },{
        "fetch":{
            "key":{
            "t":"20192018"
        }
        }
    })
    q=Q.get()
    l=trade_cal.items(query=q)
    a=list(l)
    pass

def tet_OriginConfig():
    sourceType="fixed"
    sourceConfig={
        "fixed":{
            "type":"table",
            "table":{
                "nm":"trade_cal",
                "query":{
                    "cal_date": {
                        "type": "date",
                        "restrain":"cycle", #
                        "operate": "<="
                    },
                    "is_open":1
                }
            }
        },
        "jump":{},
        "slot":{}

    }
    layer={
        "fetch":{
            "key":{
            "t":"20192018"
        }
        }
    }
    S=OriginConfig(sourceType,sourceConfig,layer)
    source=S.get()
    pass




def tet_CellRuleConfig():
    ruleType="table"
    ruleConfig={
        "table":{
            # "nm":"trade_cal",
            "query":{
                "cal_date": {
                    "type": "date",
                    "restrain":"cycle", #
                    "operate": "<="
                },
                "is_open":1
            }
        }
    }
    layer={
        "fetch":{
            "key":{
            "t":"20192018"
        }
        }
    }
    S=CellRuleConfig(ruleType,ruleConfig,layer)
    rule=S.get()
    pass