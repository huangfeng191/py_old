# -*- coding: utf-8 -*-
# Module  : 数据类型系统参数
# Author  : Liujinxiao
# Date    : 2014-8-14
# Version : 1.0

import ctx
import service
from bson.objectid import ObjectId

_db = ctx.cmdb['config']

def __db():
  
    '@rtype : pymongo.Collection'
    return _db;


def get(_id):
    return __db().find_one(_id)


def delete(cfgid):
    __db().remove({'_id':cfgid})
 

def upsert(_id, **kwArgs):
    
    s = get(_id)
    
    if s:
        
        for k,v in kwArgs.items():
            s[k] = v
    else:
        s = kwArgs
        s['_id'] = str(ObjectId())#_id
    
    __db().save(s)
    
    if(s['current']=='1'):
        for c in service.config.config.items(_id, current='1'):
            cid = c['_id']
            c.pop('_id')
            c['current'] = '0'
            service.config.config.upsert(cid, **c)
    
  
def items(_id=None, current=None):
    
    q={}
    
    if _id is not None:
        q['_id'] = {'$ne':_id}
        
    if current is not None:
        q['current'] = current
        
    return __db().find(q)
    #return __db().find({})