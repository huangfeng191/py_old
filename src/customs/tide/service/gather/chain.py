# -*- coding: UTF-8 -*-
# Module  : py
# Description : 各个单元的联结 
# Author  : Wujj
# Date    : 2020/1/31
# Version : 1.0


import  customs.tide.service.bean as bean



chain_level_up= ["cell","link","step","measure","plan"]
chain_level_down= chain_level_up.reverse()


def gatherChain(layer={},**kwargs):
    layer_level=layer.get("level")
    layer_id=layer.get("_id")
    for i, level in enumerate(chain_level_up):
        if level==layer_level:
            pass



def getCurrentLayer(layer={}):
    pass

def getChildLayers(layer={}):
    pass
    return []


def getlayerFetchById(_id):
    bean.tide_cell.get(_id )