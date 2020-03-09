# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/2/6
# Version : 1.0

from  customs.tide.service.bean import base as base
from  customs.tide.service.gather.chain import  *
from  customs.tide.service.gather.layer import  *
def test_gatherChains():
    '''
    测试 gatherChains 方法： 获取完整的 cell 链路
    Returns:

    '''
    pass
    layer = base.tide_link.get("5e391e6e3a065b4658e885e7")
    kwargs = {}
    gatherChains(layer, t=None, hook="link", **kwargs)
    print 1


def test_Class_Chains():
    '''
    测试 chain 的 上下级
    Returns:

    '''
    pass
    c_chains = Chains("5e391e6e3a065b4658e885e7", "link")
    chains = c_chains.get()
    chain = c_chains.getChainByCellId("5e391f623a065b4658e885e8")
    chain_after = c_chains.getAfterChainByCellId("5e391f623a065b4658e885e8")
    chain_front = c_chains.getFrontChainByCellId("5e391f623a065b4658e885e8")

    print "test_Class_Chains"


def test_Class_Chains_recount():
    '''
    测试 chain 的 上下级
    Returns:

    '''

    c_chains = Chains("5e391e6e3a065b4658e885e7", "link")
    c_chains.recount("hook","_id")



def test_Class_Chain():
    '''
    测试 chain level 的 上下级
    Returns:

    '''
    pass
    c_chains = Chains("5e391e6e3a065b4658e885e7", "link")
    chains = c_chains.get()
    chain = c_chains.getChainByCellId("5e391f623a065b4658e885e8")
    c_chain =Chain(chain)
    link=c_chain.getLayer("link")

    print 1

def test_Class_Layer():
    hook="cell"
    fetchKey = {
        "t": "20200208",
        "level": "cell",
        "sn": "cell_last7days",
        "levelSn": "cell_last7days",
        "cycle": "day"
    }
    layer=None
    try:
        layer=LayerLog(hook,fetchKey)
    except Exception ,e:
        print e
    print layer
    print 2