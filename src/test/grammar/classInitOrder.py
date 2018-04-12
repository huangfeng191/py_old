class A():
    def __init__(self,ax,bx):
        self.a = ax
        self.b = bx
    def f(self):
        print("ffff")
        print (self.__dict__)
    def __getattr__(self,name):
        print ("__getattr__")
    def __setattr__(self,name,value):
        print ("__setattr__")
        print ("1")
        self.__dict__[name] = value



a = A(1,2)
print "1ok"
a.f()
a.x
a.x = 3
a.f()
