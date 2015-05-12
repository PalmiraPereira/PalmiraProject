__author__ = 'Palmira Pereira'

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



point2=vector(2,2)
point1=vector(1,5)

point3=point2*2
#print (point3)
print (str(point3.x)+","+str(point3.y))