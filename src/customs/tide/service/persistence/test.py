# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/2/6
# Version : 1.0

from method import *
from customs.tide.service.persistence import *
from customs.tide.service.gather.layer import *
from pd import *
def test_Class_EmphasisTake():
    '''
    测试 chain 的 上下级
    Returns:

    '''
    hook="cell"
    o={
        "id":"5e5ba7ed3a065b37f81ab00c"
    }
    layer=None
    try:
        layer=LayerLog(hook,**o)
        take=layer.getTake()
        Emphasis=EmphasisTake(take)
        pass
        Emphasis.get()
        pass
    except Exception ,e:
        print e
    print layer
    print 2


def test_Class_PandasDo():
    source={
        "table":{
            "nm":"index_basic"
        }
    }
    rule={

    }
    carousel=None
    Pd=PandasDo(source,carousel,rule)
    Pd.go()
    print 1
