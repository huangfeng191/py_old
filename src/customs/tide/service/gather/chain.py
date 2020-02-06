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

def getChildChain(hook="plan"):
    '''
    获取chain 上的 下一级 level
    Args:
        hook:

    Returns:
        当最后一级 cell 时返回null
    '''
    child_hook=None
    if hook!="cell":
        child_hook=chain_level_up[chain_level_up.index(hook)-1]
    return child_hook


def getParentChain(hook="cell"):
    '''
    获取chain 上的 上一级 level
    Args:
        hook:

    Returns:
        当最高一级 cell 时返回null
    '''
    parent_hook=None
    if hook!="plan":
        parent_hook=chain_level_down[chain_level_down.index(hook)-1]
    return parent_hook

def gatherChains(layer,t=None,hook="plan",**kwargs):
    '''

    Args:
        layer:  {}
        t: 时间，可为空，为了数据的重复计算 以及补数据
        hook: 从那个环节开始，
        **kwargs: 暂时没用到

    Returns:

    '''
    def getHookDetail(layer,hook,chain,chains):
        '''
        取配置表里的数据，形成 chain 树
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
        chain[hook]={ "fetch":fetch,"option":option,"hookId":layer.get("_id") }
        for s in ["sn", "level","cycle"]:
            fetch[s]=layer[s]
        for s in ["refresh"]:
            option[s] = layer[s]
        child_hook=getChildChain(hook)
        if child_hook:
            l = eval(("base.tide_%s") % child_hook).items(query={"pid": layer.get("_id")}, sort=[("w", -1)])
            for one in l:
                getHookDetail(one,child_hook,chain,chains)
        else:
            chains.append(deepcopy(chain))
    def redoChain(chain,hook,t):
        '''
        对生成的树 进行二次处理，添加 默认值 : cycle refresh  ， 生成  levelSn 及 生成t
        Args:
            chain: 一条 cell的 完整 链路
            hook: level 的最高一级
            t : 时间 gatherChains 传入， 
        Returns:

        '''
        default_fill=[
            ( "fetch",[("cycle", "day")]),
            ("option",[("refresh", "refresh")])
        ]
        #  最高层 添加 默认值 ,其他层级继承父级
        for fill_k,fill_v in default_fill:
            o=chain[hook][fill_k]
            if chain.get("hook") == hook:
                for k, v in fill_v:
                    if not o.get(k):
                        o[k] = v
            else:
                parent_chain = getParentChain(hook)
                if parent_chain:
                    pO = chain[parent_chain][fill_k]
                    for k, v in fill_v:
                        if not o.get(k):
                            o[k] = pO[k]
        # 生成 levelSn
        fetch=chain[hook]["fetch"]
        level_fetch=chain[fetch.get("level", hook)]["fetch"]
        fetch["levelSn"] = level_fetch["sn"]
        # 生成 t
        fetch["t"] = tide_utils.getCycleToT(fetch.get("cycle"), t)

        child_hook=getChildChain(hook)
        if child_hook:
            redoChain(chain,child_hook,t)
        else:
            pass
    chains=[]
    chain = {"hook": hook}
    getHookDetail(layer, hook, chain,chains)
    for r in chains:
        redoChain(r,r.get("hook"),t)
    return chains



            


class Chains:
    '''
     与 chain 相关的 信息获取
    '''
    def __init__(self,_id,hook="plan" ):
       layer=eval(("base.tide_%s") % hook).get(_id)
       self.chains=gatherChains(layer,t=None, hook=hook ) or []
       self.cellIds= [r["cell"]["hookId"] for r in self.chains]

    def getChainByCellId(self,_id=""):
       chains = self.chains
       chain=None
       for r in chains:
           if r["cell"].get("hookId")==_id:
               chain=r
               break
       return chain
    def getFrontChainByCellId(self,_id):
        idx= self.cellIds.index(_id)
        chain = None
        if idx >0:
            _id=self.cellIds[idx-1]
            chain=self.getChainByCellId(_id)
        return chain
    def getAfterChainByCellId(self, _id):
        idx = self.cellIds.index(_id)
        chain = None
        if idx < len(self.cellIds)-1:
            _id = self.cellIds[idx + 1]
            chain=self.getChainByCellId(_id)
        return chain

    def getChains(self):
       chains=self.chains
       return chains


    def recount(self,hook,_id):
        chains=self.chains
        for r in chains:
            o=r[hook]
            o["option"]["refresh"]="refresh"

