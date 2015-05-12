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
def Length(u):
    return (u.x**2+u.y**2)**0.5
class edge(object):
    def __init__(self,points,point_list):
        self.point=[points[point_list[0]],points[point_list[1]]]
    length=abs(Length(self.point[0]-self.point[1]))

    midpoint=vector((self.point[1].x-self.point[0].x)/2,(self.point[1].y-self.point[0].y)/2)