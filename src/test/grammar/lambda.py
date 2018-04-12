# -*- coding: utf-8 -*-
'''
get 方法是python 自带的
'''
a={"b":1,"c":4}
print a.get("b")
print a.get("dd")
print '---------- //"1 None"'

bar = lambda:'beginman'
print bar()      #beginman
# lambda [arg1[,arg2,arg3....argN]]:expression

# lambda语句中，冒号前是参数，可以有多个，用逗号隔开，冒号右边的返回值。lambda语句构建的其实是一个函数对象。
# def add(x,y):return x+y
add2 = lambda x,y:x+y
print add2(1,2)     #3
print '---------- //"3"'
