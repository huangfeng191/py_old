# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2019/08/24
# Version : 1.0
# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2019/08/24
# Version : 1.0
import ctx
import logging
from misc import utils
import time
from datetime import datetime
from service import comm
from bson import ObjectId

from service import comm



dynamic_step = comm.CRUD(ctx.dynamicdb, "step", [("cid", 1)])

dynamic_link = comm.CRUD(ctx.dynamicdb, "link", [("cid", 1)])

dynamic_log_link = comm.CRUD(ctx.dynamicdb, "log_link", [("cid", 1)])
dynamic_log_step = comm.CRUD(ctx.dynamicdb, "log_step", [("cid", 1)])
dynamic_log_cell = comm.CRUD(ctx.dynamicdb, "log_cell", [("cid", 1)])

dynamic_link_keepFields=["generateW","ck"]

def dynamic_link_on_upsert(_id, obj, old):
        dynamic_link_keepFields=["generateW"]
        for r in dynamic_step.items(query={"link._id":_id}):
            for link in r.get("link"):
                if link.get("_id")==_id:
                    keepO={}
                    for f in dynamic_link_keepFields:
                        keepO[f]=link.get(f)
                    link.update(obj)
                    link.update(keepO)
                    dynamic_step.upsert(**r)
                    break;



def dynamic_link_on_delete(_id, obj):
    for r in dynamic_step.items(query={"link._id": _id}):
        for link in r.get("link"):
            if link.get("_id") == _id:
                r["link"].remove(link)
                dynamic_step.upsert(**r)
                break;

dynamic_link.on_upsert += dynamic_link_on_upsert
dynamic_link.on_delete += dynamic_link_on_delete

import common
import rule
import ruleFun
import ruleLink

