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

def getChildLevel(hook="plan"):
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


def getParentLevel(hook="cell"):
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
        取配置表里的数据，形成 chain 树 ,  递归配置 子一级
        Args:
            layer: hook 里的具体设置
            t:
            hook: "表"
            chain: 一个cell 的 整条 chain
            chains: 所有 cell的数组

        Returns:
            设置 chain.hook 的值 , fetch ,hookId
        '''

        fetch={
            "key":{},
            "option":{}
        }
        chain[hook]={ "fetch":fetch,"hookId":layer.get("_id"),"hook":hook }
       # 获取配置
        fetch_template=[
            ("key",["sn", "level","cycle"]),
            ( "option",["refresh","nm","pid"])
        ]
        for tK,tA in fetch_template:
            for s in tA:
                fetch[tK][s]=layer[s]


        child_hook=getChildLevel(hook)
        if child_hook:
            l = eval(("base.tide_%s") % child_hook).items(query={"pid": layer.get("_id")}, sort=[("w", -1)])
            for one in l:
                getHookDetail(one,child_hook,chain,chains)
        else:
            chain["cell"]["config"]=layer
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
        fetch_template_default=[
            ( "key",[("cycle", "day")]),
            ("option",[("refresh", "refresh")])
        ]
        #  最高层 添加 默认值 ,其他层级继承父级
        for fill_k,fill_v in fetch_template_default:
            o=chain[hook]["fetch"][fill_k]
            if chain.get("topHook") == hook:
                for k, v in fill_v:
                    if not o.get(k):
                        o[k] = v
            else:
                parent_level = getParentLevel(hook)
                if parent_level:
                    pO = chain[parent_level]["fetch"][fill_k]
                    for k, v in fill_v:
                        if not o.get(k):
                            o[k] = pO[k]
        # 生成 levelSn
        fetch_key=chain[hook]["fetch"]["key"]
        level_fetch_key=chain[fetch_key.get("level", hook)]["fetch"]["key"]
        fetch_key["levelSn"] = level_fetch_key["sn"]
        # 生成 t
        fetch_key["t"] = tide_utils.getCycleToT(fetch_key.get("cycle"), t)

        child_hook=getChildLevel(hook)
        if child_hook:
            redoChain(chain,child_hook,t)
        else:
            pass
    chains=[]
    chain = {"topHook": hook}
    getHookDetail(layer, hook, chain,chains)
    for r in chains:
        redoChain(r,r.get("topHook"),t)
    return chains



            


class Chains:
    '''
     与 chain 相关的 信息获取
     params
        hook 从那个级别开始 形成链路
        id  级别的_id
    '''
    def __init__(self,_id,hook="plan",logId=None ):
       self.logId=logId
       self.module=base.tide_chains
       layer=eval(("base.tide_%s") % hook).get(_id)
       if logId:
           log=self.module.get(logId)
           self.chains=log.get("chains")
       else:
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

    def get(self):
       chains=self.chains
       return chains
    def getLogId(self):
        return self.logId


    def recount(self,hook,_id):
        chains=self.chains
        for r in chains:
            o=r[hook]
            o["option"]["refresh"]="refresh"




class Chain:
    def __init__(self,chain):
        self.chain =chain
    def getLayer(self,level):
        
        layer=self.chain[level]
        return layer
    def getParentLayer(self,level):
        level=getParentLevel(level)
        layer=None
        if level:
            layer = self.chain[level]
        return layer
    def getChildLayer(self,level):
        level=getChildLevel(level)
        layer=None
        if level:
            layer = self.chain[level]
        return layer
    def get(self):
        return self.chain




