# -*- coding: utf-8 -*-
# Module  : 通用删除组件  all copy
# Author  : sys
# Date    : 2014-10-13
# Version : 1.0
# desc 删除的 时候，记录日志
import ctx
import misc
import time
import hashlib

_db = ctx.cmdb['deletion']

@misc.indexing(_db,
    [('id', 1)],
    [('changed',-1),('typo', 1)]
)
def __db():

    '@rtype : pymongo.Collection'
    return _db;


def upsert(typo, id, obj):  # @ReservedAssignment
  
  if typo is None or id is None or obj is None:
    return
  
  _id = hashlib.md5(repr([typo,id])).hexdigest()
  
  __db().save({
       '_id': _id ,
       'typo': typo , 
       'id': id, 
       'obj': obj, 
       'changed': int(time.time())
  })

def items(typo=None,id=None, schanged=None):  # @ReservedAssignment
  
  q = {}
  
  if typo is not None:
    if isinstance(typo, basestring):
      q['typo'] = typo
    else:
      q['typo'] = {'$in':typo}
  
  if id is not None:
    q['id'] = id
  
  if schanged is not None:
    q['changed'] = {'$gt':schanged}
    
  return __db().find(q)