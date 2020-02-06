# -*- coding: UTF-8 -*-
# Module  : py
# Description : 各个单元的联结 
# Author  : Wujj
# Date    : 2020/1/31
# Version : 1.0

from  customs.tide.service.bean import base as base
from  customs.tide.service import utils as tide_utils
from copy import deepcopy

chain_level_up= ["cell","link","step","measure","plan"]
chain_level_down= deepcopy(chain_level_up)
chain_level_down.reverse()


def gatherChains(layer,t=None,hook="plan",**kwargs):
    '''

    Args:
        layer:  {}
        t: 时间，可为空，为了数据的重复计算 以及补数据
        hook: 从那个环节开始，
        **kwargs: 暂时没用到

    Returns:

    '''
    def getHookDetail(layer,t,hook,chain,chains):
        '''

        Args:
            layer: hool 里的具体设置
            t:
            hook: "那个表开始"
            chain: 一个cell 的 整条 chain
            chains: 所有 cell的数组

        Returns:

        '''
        fetch={}
        option={}
        chain[hook]={ "fetch":fetch,"option":option }
        for s in ["sn", "level","cycle"]:
            fetch[s]=layer[s]
        fetch["t"]=tide_utils.getCycleToT(fetch.get("cycle"),t)

        for s in ["refresh"]:
            option[s] = layer[s]

        if hook!="cell":
            child_hook=chain_level_up[chain_level_up.index(hook)-1]
            l = eval(("base.tide_%s") % child_hook).items(query={"pid": layer.get("_id")}, sort=[("w", -1)])
            for one in l:
                getHookDetail(one,t,child_hook,chain,chains)
        else:
            chains.append(deepcopy(chain))
    def redoChain(chain,hook):
        '''

        Args:
            chain: 一条 cell的 完整 链路
            hook: level 的最高一级

        Returns:

        '''
        fetch=chain[hook]["fetch"]
        level_fetch=chain[fetch.get("level", hook)]["fetch"]
        fetch["levelSn"] = level_fetch["sn"]
        if hook!="cell":
            child_hook=chain_level_up[chain_level_up.index(hook)-1]
            redoChain(chain,child_hook)
        else:
            pass
    chains=[]
    chain = {"hook": hook}
    getHookDetail(layer, t, hook, chain,chains)
    for r in chains:
        redoChain(r,r.get("hook"))
    return chains



# TODO:  cycle  refresh  extend   考虑在 redoChain 中实现
            

def test_gatherChains():
    pass
    layer=base.tide_link.get("5e391e6e3a065b4658e885e7")
    kwargs={}
    gatherChains(layer, t=None, hook="link", **kwargs)
    print 1




def getCurrentLayer(layer={}):
    pass

def getChildLayers(layer={}):
    pass
    return []


def getlayerFetchById(_id):
    pass
    # bean.tide_cell.get(_id )