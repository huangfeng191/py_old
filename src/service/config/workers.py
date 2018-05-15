# -*- coding: utf-8 -*-
# Module  : 分布式服务组件
# Author  : Lijiajie
# Date    : 2016-02-21
# Version : 1.0

import ctx
import misc
import logging
import time

import socket

ipaddr = None

try:
  ipaddr = socket.gethostbyname(socket.getfqdn())
except:
  ipaddr = "127.0.0.1"

_db = ctx.cmdb['workers'];

@misc.indexing(_db, [('changed',1)])
def __db():
    
    '@rtype : pymongo.Collection'
    return _db;

def items():
  
  return list(__db().find({'changed': {'$gte': time.time() - 300}}))

def sync(workers, current):
  
  try:
    
    logging.info("Synchronizing workers...")
    
    __db().remove({'changed': {'$lte': current - 300}})
    
    for worker in workers:
      
      __db().save({
          
          '_id'   :  worker.id, 
          'name'  :  worker.name,
          'state' :  worker.state,
          'type'  :  worker.type,
          'reboot':  worker.reboot,
          'protect': worker.protect,
          'changed': current,
          'sys'  :   worker.sys,
          'pid'  :   worker.pid, 
          'ip'   :   ipaddr,
      })
      
      
    logging.info("Done.")
    
  except Exception, e:
    
    logging.error(e)
