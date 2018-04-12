# -*- coding: UTF-8 -*-

n1=1

if n1:
    print "1 is true "
n2=0

if not n2:
   print "0 is false  "  

o1={"z1":""}   

print "o1.get('z1',?)==\"\":%s"%(o1.get("z1",u"空字符串不会被替换")) 
print "o1.get('z1',?)==\"\":%s"%(o1.get("z2",u"对象中找不到的key会被替换")) 