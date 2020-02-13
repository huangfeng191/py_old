# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/2/6
# Version : 1.0


from customs.tide.service.utils import *

def test_chip_method(query):
    print "step 1 is Ok "
    print query
def test_contactToMethod():
    s="test_chip_method"
    query={"query":{"$match":"sf"}}
    s_method=contactToMethod(s,query )
    eval(s_method)