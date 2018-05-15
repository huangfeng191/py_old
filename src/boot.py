# -*- coding: UTF-8 -*-
# Module  : boot
# Description : 启动脚本
# Author  : fengfeng
# Date    : 2018-05-04
# Version : 1.0

import os,site
site.addsitedir(os.path.join(os.getcwd(), '..', 'lib'))

import PlatLib  # 添加平台环境变量


import sys
reload(sys)
sys.setdefaultencoding("utf-8")  # @UndefinedVariable
import time

# mongo 信息
import service  # @UnusedImport-

# 2018-05-04

from server import center
import ui
from clients import hdworker
from service.config import codes


def wrapsys(_id = None, fun = None, mode = None,name = None,module = None,In = None,Out = None, args={}):
    
    sv = codes.get(_id) or {}
    
    conf = {}
    
    conf['module'] = module
    conf['id'] = _id
    conf['in'] = In
    conf['out'] = Out
    
    for k,v in args.items():
        conf[k] = v
        
    par = {
           
       'name':name,
       'mode':(sv.get('mode') or mode),
       'protect':True,
       'auto':True,
       'in':In,
       'out':Out,
       'ds':None,
       'type':1,
       'num':sv.get('num', 1),
       'codes':''
    }
    
    codes.upsert(_id,Type = 1, **par)
    
    for _ in xrange(0, int(sv.get('num',1))):
        center.spawn(par.get('mode'), fun, name,kwArgs={'config':conf} if fun == hdworker.main else {})

def main():

    center.main()

    ui.main()


def _main():
    main()

    while True:
        time.sleep(2 ** 20)
if __name__ == "__main__":
    _main()
