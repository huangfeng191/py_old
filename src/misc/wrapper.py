# -*- coding: UTF-8 -*-
# Module  : py
# Description :slef reuse warpper
# Author  : Wujj
# Date    : 2019/09/03
# Version : 1.0
import reuse as reuse
import json


def calc_runtime_wrapper_noText(func):
    import time

    def wrap(**kwArgs):
        st=time.time()
        print "runtime startCount"
        res=func(**kwArgs)
        print "runtime endCount:%f second " % ((time.time() - st))
        return res
    return wrap


" tip: 直接调用一次，可以锁定内部变量 text "
def calc_runtime_wrapper(text="no set "):
    def decorator(func):
        import time
        def wrap(**kwArgs):
            st=time.time()
            print "method:%s runtime  startCount"%text
            res=func(**kwArgs)
            print "method:%s runtime  endCount:%f" % (text,(time.time() - st))
            return res
        return wrap
    return decorator

# 多次调用时 监视进度用
def loop_fun_wrapper(text="loop_fun_wrapper ",times=100):
    def decorator(func):
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
            if a_count[0] %times==0:
                print "method %s execute %d  times: continue:%f second"%(text,times,a_continue[0])
                a_continue[0]=0

            a_continue[0]=a_continue[0]+time.time()-st
            return res
        return wrap
    return decorator


def loop_fun_reset_wrapper(func):
    def wrap(**kwArgs):
        print "reset count over"
        kwArgs["resetCount"]={"valid":1}
        res=func(**kwArgs)

        return res
    return wrap







# test instance 
@calc_runtime_wrapper("test ")
def run_times(**kwArgs):
    print "OK"




