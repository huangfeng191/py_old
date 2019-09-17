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
        print "startCount"
        res=func(**kwArgs)
        print "endCount:%f" % (time.time() - st)
        return res
    return wrap


# 多次调用时 监视进度用
def loop_fun_wrapper(func):
    import time
    a_count=[0]
    a_continue=[0]
    def wrap(**kwArgs):
        if kwArgs.get("resetCount") and kwArgs["resetCount"]["valid"]:
            a_count[0]=0
            kwArgs["resetCount"]["valid"]=0
        st=time.time()
        res=func(**kwArgs)
        a_count[0] = a_count[0] + 1
        if a_count[0] %100==0:
            print "continue:%f"%(a_continue[0])
            a_continue[0]=0

        a_continue[0]=a_continue[0]+time.time()-st
        return res
    return wrap


def loop_fun_reset_wrapper(func):
    def wrap(**kwArgs):
        print "reset count over"
        kwArgs["resetCount"]={"valid":1}
        res=func(**kwArgs)

        return res
    return wrap







# test instance 
@calc_runtime_wrapper
def run_times(**kwArgs):
    print "OK"




