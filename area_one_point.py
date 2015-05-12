__author__ = 'Palmira Pereira'
from math import *
class vector(object):
    def __init__(self,x,y):
        self.x=float(x)
        self.y=float(y)
    def __add__(self,v):
        return vector(self.x + v.x, self.y + v.y )
    def __sub__(self,v):
        return vector(self.x - v.x, self.y - v.y )
    def __mul__(self,val):
        return vector(val*self.x,val*self.y)
def Dot(u,v):
    return u.x*v.x+v.y*u.y
def Length(u):
    return (u.x**2+u.y**2)**0.5

u=vector(-100,-100)
v=vector(-1,1)
radius=1.5
m=(u.y-v.y)/(u.x-v.x)
print (m)
b=u.y-m*u.x
print(b)
x1=(-2*m*b-sqrt((2*m*b)**2-4*(1+m**2)*(b**2-radius**2)))/2/(1+m**2)
temp_vector=vector(x1,x1*m+b)
print (Length(u-temp_vector)+Length(v-temp_vector))
print (Length(u-v))
if (abs(Length(u-temp_vector)+Length(v-temp_vector)-Length(u-v)))<=0.0001:
    print (x1)
    print (x1*m+b)
else:
    x1=(-2*m*b+sqrt((2*m*b)**2-4*(1+m**2)*(b**2-radius**2)))/2/(1+m**2)
    print (x1)
    print (x1*m+b)
sin