# -*- coding: utf-8 -*-

""" 
此模式 会在启动的时候就调用

 """
def foo():
    print "in foo()"
foo()    

print "down --------------"
import time

def foo111():
    st=time.time()
    print "in foo()"
    print time.time()-st
foo111()      


def foo112(func):
    st=time.time()
    func()
    print time.time()-st
   
print "包装模式↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓--down" 

def fooCs():
    print "is foo"

def timeIt(func):
    start=time.time()
    func()
    end=time.time()
    print end-start
timeIt(fooCs)
print "此方法修改了调用的方法↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑--up" 


print "↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓--down" 

def foo1():
    print "is foo"
def timeIt1(func):
    def wrapper():
        start=time.time()
        func()
        end=time.time()
        print end-start
    return wrapper
foo1= timeIt1(foo1)   
foo1()


print "语法糖↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓--down" 

def timeIt2(func):
    def wrapper():
        start=time.time()
        func()
        end=time.time()
        print end-start
    return wrapper
@timeIt2    
def foo2():
    print "is foo"

foo2()
