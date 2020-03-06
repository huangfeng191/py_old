# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/3/6
# Version : 1.0


" tip: 直接调用一次，可以锁定内部变量 text "
def runtime_wrapper(text="no set "):
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


def runtime_wrapper_noText(func):
    import time

    def wrap(**kwArgs):
        st=time.time()
        print "runtime startCount"
        res=func(**kwArgs)
        print "runtime endCount:%f second " % ((time.time() - st))
        return res
    return wrap