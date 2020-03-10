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
       self.module=base.tide_chains_log
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




    def getInfectHook(self,chain,before_chain):
        '''

        '''
        C=Chain(chain)
        infect=chain.get("topHook")
        while infect:
            layer_chain= chain[infect]
            layer_before= before_chain[infect]
            if tide_utils.equalObj(layer_chain.get("fetch").get("key"),layer_before.get("fetch").get("key")):
                layer=C.getChildLayer(infect)
                if layer:
                    infect= layer.get("hook")
            else:
                infect=layer_chain.get("hook")
                break
        return infect

    def getObj(self):
        '''
        获取Ojbect 类型的 chains
        Returns:

        '''
        chains=self.chains
        o=None
        for i in range(0,len(chains)):
            chain=chains[i]
            o_chain=Chain(chain)
            if i==0:
                topHook = chain.get("topHook")
                o = chain.get(topHook)
                self.getChildren(o_chain, o)
            else:
                before_chain= chains[i-1]
                hook=self.getInfectHook(chain,before_chain)
                layer=chain[hook]

                #  if  layer.hook == o.hook  不可能 因为 这种情况 只有指定 cell 不可能存在层级

                data=o.get("children") or []
                while len(data)>0:
                        dim=data[-1]
                        if dim.get("hook")==hook:
                            data.append(layer)
                            # 再相应级别上添加数据
                            self.getChildren(o_chain,layer)
                            data=[]
                        else:
                            data = dim.get("children") or []


        return o

    def getLayersByHook(self,hook,pid=""):
        pass
        chains=self.chains
        ret=[]
        for r in chains:
            layer=r.get(hook)
            if layer.get("fetch").get("option").get("pid")==pid:
                exists=False
                for r1 in ret:
                    if tide_utils.equalObj(layer.get("fetch").get("key"),r1.get("fetch").get("key")):
                        exists=True
                        break
                if not exists:
                    ret.append(layer)
        return ret




    def getChildren(self,chain,o):
        hook=o.get("hook")
        if "children" not in o:
            o["children"]=[]
        children=o.get("children")
        layer=chain.getChildLayer(hook)
        if layer:
            if "children" not in layer:
                layer["children"]=[]
            children.append(layer)
            self.getChildren(chain,layer)





# 上下级比较 如果 不同 或最后一个 保存数据，获取下一级 直至循环结束，组成的对象就是需要的结果用 children 组装
# 需要获取那一级 指定






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




