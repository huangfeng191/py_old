# -*- coding: UTF-8 -*-
# Module  : py
# Description :slef reuse warpper
# Author  : Wujj
# Date    : 2019/09/03
# Version : 1.0
import reuse as reuse
import json

def calc_runtime_wrapper(func):
    import time
    def wrap(**kwArgs):
        st=time.time()
        res=func(**kwArgs)
        print "continue:%f"%(time.time()-st)
        return res
    return wrap







# test instance 
@calc_runtime_wrapper
def run_times(**kwArgs):
    print "OK"




