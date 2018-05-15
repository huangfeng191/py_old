# -*- coding: utf-8 -*-
# Module  : clients.hdworker
# Author  : Lijiajie
# Date    : 2014-7-2
# Version : 1.0

import ctx
import time

import importlib
from service.config import codes
import misc

import threading

lock = threading.Lock()

INITED = set([])

def main(config):
  
    global INITED, lock
    
    MODULE = config['module']
    
    module = importlib.import_module(MODULE)
    
    ID = config.get("id",None) # 当前总线名字
    
    FUNCTIONS = dir(module)
    
    if 'init' in FUNCTIONS:
      
      if '_inited_' not in FUNCTIONS:
      
        try:
          
          lock.acquire()
          
          if MODULE not in INITED:
            module.init(**config)
            INITED.add(MODULE)
        
        finally:
          
          module._inited_ = True
          lock.release()
        

    IN  = config.get('in' , None)
    OUT = config.get('out' , None)
    
    if not 'main' in FUNCTIONS:
        time.sleep(10.0)
        return True
    
    if not IN and not OUT:
        
        module.main()
        return False
    
    if OUT and isinstance(OUT, basestring):
        OUT = [OUT]
    
    while True:
        
        data = True
        
        while data:
            
            val = ctx.bus.recv(IN) or None
            
            if val is not None:
                
                r = module.main(*val)
                
                if OUT and r is not None:
                    for O in OUT: ctx.bus.send(O, r)
                
                if ID is not None and r is not None:
                    
                    sv = misc.cache("CODES-ITEMS", ID, lambda:list(set([ k['in'] for k in codes.items(DataSource=ID, Fields=["in"])])), ctx.CACHE_TTL)
                    for O in sv :
                        ctx.bus.send(O, r)
            else:
                data = False

        # 采用了blpop之后，可以不再sleep，提升性能指数
        # time.sleep(0.4)