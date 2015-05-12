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
class edge(object):
    l=3 #length of triangle
    h=3 #number of rows
    n=3 #number of columns
    def __init__(self,points):
        self.points=points
        #init_edge()
    def init_edge(self):
        h_edges=[]
        v_for_edges=[]
        v_back_edges=[]
        for i in range(h):
            for j in range(n-1):
                h_edges.append([j+n*i,j+1+n*i])

        for j in range(h-1):
            if j%2==0:
                for i in range(n-1):
                    v_for_edges.append([n*j+i,n*j+i+n])
                v_for_edges.append([j*n+n-1,j*n+n+n-1])
            else:
                for i in range(n-1):
                    v_for_edges.append([n*j+i,n*j+i+n+1])

        for j in range(h-1):
            if j%2==1:
                for i in range(n-1):
                    v_back_edges.append([n*j+i,n*j+i+n])
                v_back_edges.append([n*j+n-1,n*j+n-1+n])
            else:
                for i in range(n-1):
                    v_back_edges.append([n*j+1+i,n*j+1+n-1+i])
        edges=[]

        for i in h_edges:
            edges.append(i)
        for i in v_for_edges:
            edges.append(i)
        for i in v_back_edges:
            edges.append(i)
        self.edges=edges


def Dot(u,v):
    return u.x*v.x+v.y*u.y
def Length(u):
    return (u.x**2+u.y**2)**0.5
def create_text(n,h,points):
    text_file = open("triangle_upload_new.dat", "w")
    text_file.write("TITLE=\"TRIANGLE UPLOAD NEW\"\n")
    text_file.write("VARIABLES= \"X\",\"Y\"\n")
    text_file.write("ZONE N=")
    text_file.write(str(len(points)))
    text_file.write(", E=")
    text_file.write(str(n*2-2+(2*n-2)*(h-2)))
    text_file.write(",F=FEPOINT ET=Triangle\n")

    for j in range(h):
        for i in range(n):
            text_file.write (str(points[n*j+i].x)+" "+str(points[n*j+i].y)+"\n")
    text_file.write ("\n")

    for j in range(h-1):
        if j%2==0:
            for i in range(n-1):
                text_file.write (str(i+j*n+1)+" "+str(i+j*n+2)+" "+str(i+j*n+n+1)+"\n")
        else:
            for i in range(n-1):
                text_file.write (str(i+j*n+1)+" "+str(i+j*n+2)+" "+str(i+j*n+n+2)+"\n")
    for j in range(h-1):
        if j%2==0:
            for i in range(n-1):
                text_file.write (str(i+j*n+2)+" "+str(i+j*n+n+1)+" "+str(i+j*n+n+2)+"\n")
        else:
            for i in range(n-1):
                text_file.write (str(i+j*n+1)+" "+str(i+j*n+n+1)+" "+str(i+j*n+n+2)+"\n")
def create_points(h,n,l):
    temp=0
    points=[]
    for j in range(h):
        for i in range(n):
            points.append(vector(i*l+temp*l/2,j*l))
        if temp==0:
                temp=1
        else:
            temp=0
    return points

#variables
l=3 #length of triangle
h=3 #number of rows
n=3 #number of columns

points=create_points(h,n,l)
create_text(n,h,points)



test=edge(points)

print (test.points)

