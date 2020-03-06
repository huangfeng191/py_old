# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/3/6
# Version : 1.0


" tip: 直接调用一次，可以锁定内部变量 text "
def runtime_wrapper_func(text="no set "):
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





# for class


" tip: 直接调用一次，可以锁定内部变量 text "
def runtime_wrapper(text="no set "):
    def decorator(func):
        import time
        def wrap(self, *args, **kwArgs):
            st=time.time()
            print "method:%s runtime  startCount"%text
            res=func(self, *args, **kwArgs)
            print "method:%s runtime  endCount:%f" % (text,(time.time() - st))
            return res
        return wrap
    return decorator







# 多次调用时 监视进度用
# 父方法调用
def runtime_times_wrapper_reset(func):
    def wrap(self, *args, **kwArgs):

        kwArgs["resetCount"]={"valid":1}

        res=func(self, *args, **kwArgs)
        return res
    return wrap

# 计时方法调用
def runtime_times_wrapper(text="loop_fun_wrapper ",times=100):
    def decorator(func):
        import time
        a_count=[0]
        a_continue=[0]
        a_all=["unknown"]
        def wrap(self, *args, **kwArgs):

            if kwArgs.get("resetCount") and kwArgs["resetCount"]["valid"]:
                print "method %s  开始循环计数-------------------------"%(text)
                a_count[0]=0
                a_all[0]=kwArgs["resetCount"]["all"]  if kwArgs["resetCount"].get("all")  else "unknown"
                kwArgs["resetCount"]["valid"]=0
            st=time.time()
            res=func(self, *args, **kwArgs)
            a_count[0] = a_count[0] + 1
            if a_count[0] %times==0:
                print "method %s execute ( %d / %s ) ---%s times continue:%f second"%(text ,a_count[0],a_all[0],times,a_continue[0])
                a_continue[0]=0
            a_continue[0]=a_continue[0]+time.time()-st
            return res
        return wrap
    return decorator








