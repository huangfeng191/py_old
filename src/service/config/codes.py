# -*- coding: utf-8 -*-
# Module  : 自定义服务
# Author  : Lijiangfeng
# Date    : 2014-7-7
# Version : 1.0

import ctx
from _io import open
import codecs
import base64
import contextlib
import misc

_db = ctx.cmdb['%s%s%s' % (ctx.ND_PREFIX, '' if not ctx.ND_PREFIX else '_', 'codes')]

@misc.indexing(_db, [('ds',1)])
def __db():
    
    '@rtype : pymongo.Collection'
    return _db;

def get(_id):
    
    item = __db().find_one(_id)
    return item
  
@misc.deletion('codes')
def delete(_id):
    
    obj = get(_id)
    if obj: __db().remove({'_id':_id})
    return obj

def upsert(_id, Type = None, **kwArgs):

    s = get(_id)

    if s:
        for k,v in kwArgs.items():
            s[k] = v
    else:
        s = kwArgs
        s['_id'] = _id
    
    if s.get('ds') is not None:
        s['in'] = _id
    
    if Type is None or Type == 2:
        _creatfile(s)    
 
    __db().save(s)

def _creatfile(data):
    
    path = "clients/ext/%s%s" % (data["_id"], data.get("suffix",".py"))
    
    with contextlib.closing(codecs.open(path,"wb")) as f:
        f.write(base64.decodestring(data['codes']))

def _getfile(_id):
    
    path ="clients/ext/%s.py" % _id
    
    f = open(path)
    
    try:
        codes = f.read()
    finally:
        f.close();
    return codes



def items(DataSource=None,Fields=None,Type = None):
    
    '''
    @param DataSource: 指定数据源
    @param Fields: 过滤的字段列表
    @param Type: 类型   1：系统服务    2：用户服务   
    '''
    q = {}
    
    if Type is not None:
        q['type'] = Type
        
    if DataSource is not None:
        q['ds'] = DataSource
    
    return __db().find(q,projection=Fields)

