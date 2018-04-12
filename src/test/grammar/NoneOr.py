# -*- coding: utf-8 -*-
a=None
if not a :
    a=0
    print "111 "+ str(a)
if not a:
   a=1
   print "222 "+ str(a)
if not a:
   a=1
   print "333 "+ str(a)
b={}

print b.get("a")
print b.get("a")==None
print "--111 0---222 1-----None--True-------"
#  0  根 None 都是false ,  None>=0 false None<0 true
if b.get("c")>=0:
    print 1
if b.get("c")<0:
    print 2   
if b.get("c")==None:
    print 3    
else:
   print 4  
print "---2-3--------"

if None<0:
  print 2
else:
  print 4 
print "---2--------"

print (0 or 1)
print "---1----//类似三木运算符----"


print None==False

print "---None==False----//return false----"


a={}
if a:
  print 1
else:
  print 2
print "---//2----"   