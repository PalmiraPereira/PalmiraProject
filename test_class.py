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

class edge(object):
    def __init__(self,points,point_list):
        self.point=[points[point_list[0]],points[point_list[1]]]
    def length(self):
        return abs(Length(self.point[0]-self.point[1]))
    def mid_point(self):
        return vector((self.point[1].x-self.point[0].x)/2,(self.point[1].y-self.point[0].y)/2)
class triangle(object):
    def __init__(self,point,point_list,height):
        self.point=[points[point_list[0]],points[point_list[1]],point[point_list[2]]]
        self.height=height
    def area(self):
        return self.height*self.height/2
    def centroid (self):
        return vector((self.point[1].x+self.point[0].x+self.point[2].x)/3,(self.point[1].y+self.point[0].y+self.point[2].y)/3)
class unstructured_mesh(object):
    def __init__(self,points,l,h,n):
        self.points=points
        self.l=l
        self.h=h
        self.n=n
    def edges(self):
        h=self.h
        n=self.n
        edges=[]
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

        for i in h_edges:
            edges.append(i)
        for i in v_for_edges:
            edges.append(i)
        for i in v_back_edges:
            edges.append(i)
        return edges
    def triangles(self):
        h=self.h
        n=self.n
        triangle_up=[]
        triangle_down=[]
        triangles=[]
        for j in range (h-1):
            for i in range(n-1):
                if j%2==0:
                    triangle_up.append([i+j*n,i+j*n+1,n+i+j*n])
                else:
                    triangle_up.append([i+j*n,i+j*n+1,n+i+j*n+1])
        for j in range (h-1):
            for i in range (n-1):
                if j%2==0:
                    triangle_down.append([i+1+j*n,n+i+n*j,n+i+n*j+1])
                else:
                    triangle_down.append([i+j*n,n+i+n*j,n+i+n*j+1])
        for j in range(h-1):
            for i in range(n-1):
                if j%2==0:
                    triangles.append(triangle_up[i+j*(n-1)])
                    triangles.append(triangle_down[i+j*(n-1)])
                else:
                    triangles.append(triangle_down[i+j*(n-1)])
                    triangles.append(triangle_up[i+j*(n-1)])
        return triangles

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
def create_text(n,h,points):
    text_file = open("triangle_upload_new.dat", "w")
    text_file.write("TITLE=\"TRIANGLE UPLOAD NEW\"\n")
    text_file.write("VARIABLES= \"X\",\"Y\",\"Volume Fraction\"\n")
    text_file.write("ZONE N=")
    text_file.write(str(len(points)))
    text_file.write(", E=")
    text_file.write(str(n*2-2+(2*n-2)*(h-2)))
    text_file.write(",F=FEPOINT ET=Triangle\n")

    for j in range(h):
        for i in range(n):
            text_file.write (str(points[n*j+i].x)+" "+str(points[n*j+i].y)+" 0\n")
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
def find_edges_in_triangle(edges,triangles):
    edges_in_triangle=[]
    for j in range(len(triangles)):
        temp_edges_in_triangle=[]
        temp_triangle=triangles[j]
        for i in range(len(edges)):
            if ([temp_triangle[1],temp_triangle[0]]==[edges[i][0],edges[i][1]])or([temp_triangle[0],temp_triangle[1]]==[edges[i][0],edges[i][1]]) :
                temp_edges_in_triangle.append(i)
            if ([temp_triangle[1],temp_triangle[2]]==[edges[i][0],edges[i][1]])or([temp_triangle[2],temp_triangle[1]]==[edges[i][0],edges[i][1]]) :
                temp_edges_in_triangle.append(i)
            if ([temp_triangle[2],temp_triangle[0]]==[edges[i][0],edges[i][1]])or([temp_triangle[0],temp_triangle[2]]==[edges[i][0],edges[i][1]]) :
                temp_edges_in_triangle.append(i)
        edges_in_triangle.append(temp_edges_in_triangle)
    return edges_in_triangle
l=3 #length of triangle
h=3 #number of rows
n=3 #number of columns

points=create_points(h,n,l)
create_text(n,h,points)
test=unstructured_mesh(points,l,h,n)

