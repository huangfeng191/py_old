# -*- coding: UTF-8 -*-
# Module  : clients.hdbus
# Description : 服务中心
# Author  : lijiajie@chinahddz.com
# Date    : 2014-05-05
# Version : 1.0

from multiprocessing.process import Process
from threading import Thread
import uuid
import logging
import time
from service.config import codes
import service.config.workers
from clients import hdworker
from bson import ObjectId
import copy
import base64
import os
import psutil

def process_loop(m, *args,**kwArgs):
    
    
    p = psutil.Process(os.getpid())
    ppid = None
    
    if not isinstance(p.ppid, int):
        ppid = p.ppid()
    else:
        ppid = p.ppid
    
    if ppid > 0:
        
        p = psutil.Process(ppid)
        
        def check():
            
            if not p.is_running():
                logging.error("Parent dead, exiting...")
                os._exit(-1)
        
        import schedule
        schedule.logger.setLevel('WARN')
        schedule.every(1).seconds.do(check)
        
        def __check():

            while True:
                schedule.run_pending()
                time.sleep(0.5)
        
        Thread(target=__check).start()

    return m(*args,**kwArgs)

class Worker(object):
    
    def is_alive(self):
        return self.m and self.m.is_alive()


class ProcessWorker(Worker):
    
    def __init__(self, target, name=None, args=(),kwArgs={}, protect=True, sys = True , cid = None):

        self.id = uuid.uuid4().get_hex()
        if cid is not None: self.id = cid
        
        self.name = name
        self.target = target
        self.args = args
        self.type='Process'
        self.kwArgs = kwArgs
        self.protect=protect
        self.state ='PENDING'
        self.reboot=-1
        self.sys = sys
        self.m = None
    
    @property
    def pid(self):
      
      return self.m.pid
    
    def start(self):
        
        import importlib
        
        if isinstance(self.target, basestring):  
            m = importlib.import_module(self.target)
        else:
            m = self.target
        
        
        self.m = Process(target=process_loop,name=self.name,args=(m,) + self.args,kwargs=self.kwArgs)
        self.m.daemon = True
        
        try:

            import ctx
            ctx.mdb.close()

            self.m.start()
            self.state ='RUNNING'
            self.reboot+=1
        except Exception, e:
            self.state ='ABORT'
            logging.exception(e)
    
    def terminate(self):
        self.state ='PENDING'
        if self.m is not None:
            self.m.terminate()

class ThreadWorker(Worker):
    
    def __init__(self, target, name=None, args=(),kwArgs={}, protect=True, sys = True, cid = None):

        self.id = uuid.uuid4().get_hex()
        if cid is not None:
            self.id = cid;
        self.name = name
        self.target = target
        self.type='Thread'
        self.args = args
        self.kwArgs = kwArgs
        self.protect=protect
        self.state ='PENDING'
        self.reboot=-1
        self.sys = sys
        self.m = None
        self.pid = os.getpid()
    
    def start(self):
        
        import importlib
        
        if isinstance(self.target, basestring):  
            m = importlib.import_module(self.target)
        else:
            m = self.target
        
        self.m = Thread(target=m,name=self.name,args=self.args,kwargs=self.kwArgs)
        
        try:
            self.m.start()
            self.state ='RUNNING'
            self.reboot+=1
        except Exception, e:
            self.state ='ABORT'
            logging.exception(e)
            
    def terminate(self):
#         self.state ='PENDING'
#         self.m.terminate()
        logging.warn("Cannot terminate thread.")

workers = []

def spawn(mode='process', target=None, name=None, args=(),kwArgs={}, protect=True, sys = True, auto=True,cid = None):
    
    if target is None:
        raise Exception("No target specified!")

    if mode == 'process':
        m = ProcessWorker(target=target, name=name, args=args, kwArgs=kwArgs, protect=protect,sys = sys,cid = cid);
        workers.append(m)
    elif mode == 'thread':
        m = ThreadWorker(target=target, name=name, args=args, kwArgs=kwArgs, protect=protect, sys = sys, cid = cid);
        workers.append(m)
    else:
        raise Exception("Unkown mode `%s`" % mode)
    
    if auto:
        m.start()
    

def proc_killall():
    
    for worker in workers:
        if isinstance(worker, ProcessWorker):
            worker.terminate()

def protect():
    
    i = 1
    
    while(True):
        
        for worker in workers:
            
            if worker.protect and worker.state == 'RUNNING' and not worker.is_alive():
                logging.error("Worker dead ... %s(%s)" % (worker.name, worker.id))
                worker.start()
                logging.error("Worker restarted ... %s(%s)" % (worker.name, worker.id))
            elif worker.state == 'ABORT':
                worker.state = 'HALT'
                logging.error("Worker aborted ... %s(%s)" % (worker.name, worker.id))
        
        if i % 12 == 0:
          service.config.workers.sync(workers, time.time())
          
        i = i + 1
        time.sleep(5.0)

#添加服务
def addservice(_id, name,mode, protect,auto,content,In = None,Out = None,ds = None,Type = 2):
    
    content = base64.encodestring(content)
    
    sv = {'_id':_id,'name':name,'mode':mode,'protect':protect,'auto':auto,'codes':content,'in':In,'out':Out,'ds':ds,'type':Type}
    
    par = copy.copy(sv)
    del par['_id']
    codes.upsert(_id,**par)
    
    conf = {
        'module': "clients.ext.%s" % sv['_id'],
        'id':sv['_id']
    }
        
    if sv.get('in') is not None:
        conf['in'] = sv['in']
        
    spawn(sv['mode'],hdworker.main,sv['name'],kwArgs={
        'config':conf
    },protect=False, sys = False, auto= False)

#启动服务
def startservice(_id):

    sv = codes.get(_id)
    wk = filter(lambda x:x.id == _id, workers)
    
    #用户自定义服务
    if sv is not None:
        
        if len(wk)>0:
            wk[0].terminate()
            workers.remove(wk[0])
        
        codes._creatfile(sv)
        conf = {
            'module': "clients.ext.%s" % sv['_id'],
            'id':sv['_id']
        }
        
        if sv.get('in') is not None:
            conf['in'] = sv['_id']
            
        spawn(sv['mode'],hdworker.main,sv['name'],kwArgs={
        
                'config':conf
            },protect = sv['protect'], sys = False, auto = True,cid = sv['_id'])
    
    #系统服务
    elif wk is not None and len(wk)>0 and wk[0].state !='RUNNING':
        
        wk[0].start()

#停止服务
def stopservice(_id):
    
    wk = filter(lambda x:x.id == _id, workers)
    
    if wk is not None and len(wk)>0:
        wk[0].terminate()
    return wk
    

#重启自定义服务
def restart(_id):
    
    sv = codes.get(_id)
    if sv is not None:
        stopservice(_id)
        startservice(_id)

#删除自定义服务
def deleteservice(_id):
    
    wk = stopservice(_id)
    
    if wk is not None and len(wk)>0:
        workers.remove(wk[0])
        
    codes.delete(codeid = _id)

#扩容服务
def extendservice(_id):
    
    sv = codes.get(_id)
    if sv is not None:
        #自定义服务

        csv = copy.copy(sv)
        sid = ObjectId().__str__()
        csv['_id'] = sid
        if csv['in'] is not None:
            csv['in'] = sid
        addservice(_id = csv['_id'], name = csv['name'],mode = csv['mode'], protect = csv['protect'],auto = csv['auto'],content = csv['codes'],In = csv['in'],Out = csv['out'],ds = csv['ds'])
        
    else:
        #系统服务
        wk = filter(lambda x:x.id == _id, workers)
        if wk is not None and len(wk)>0:
            extwk = copy.copy(wk[0])
            extwk.reboot = -1
            workers.append(extwk)
            extwk.start()
            
            sv = codes.get(extwk.name)
            if sv is not None:
                par = {'num':sv.get('num',1)+1}
                codes.upsert(extwk.name,Type = 1, **par)
            
def main():
    
    spawn('thread', protect, 'watchdog')