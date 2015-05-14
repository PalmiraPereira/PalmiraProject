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

class edge(object):
    def __init__(self,points,point_list):
        self.point=[points[point_list[0]],points[point_list[1]]]
    def length(self):
        return abs(Length(self.point[0]-self.point[1]))
    def mid_point(self):
        return vector((self.point[1].x-self.point[0].x)/2,(self.point[1].y-self.point[0].y)/2)
class triangle(object):
    def __init__(self,points,point_list,height):
        self.point=[points[point_list[0]],points[point_list[1]],points[point_list[2]]]
        self.height=height
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
def create_text(n,h,points,triangles,volume_fraction,normal_x,normal_y):
    text_file = open("triangle_upload_new.dat", "w")
    text_file.write("TITLE=\"TRIANGLE UPLOAD NEW\"\n")
    text_file.write("VARIABLES= \"X\",\"Y\",\"Volume Fraction\",\"U\",\"V\"\n")
    text_file.write("ZONE\nDataPacking=Block\nZoneType=FETRIANGLE\n")
    text_file.write("N=")
    text_file.write(str(len(points)))
    text_file.write(" E=")
    text_file.write(str(n*2-2+(2*n-2)*(h-2)))
    text_file.write("\nVARLOCATION=([3-5]=CELLCENTERED)\n")

    for i in range(len(points)):
            text_file.write (str(points[i].x)+" ")
    text_file.write ("\n")
    for i in range(len(points)):
            text_file.write (str(points[i].y)+" ")
    text_file.write ("\n")
    for i in range(len(volume_fraction)):
            text_file.write (str(volume_fraction[i])+" ")
    text_file.write ("\n")
    for i in range(len(normal_x)):
            text_file.write (str(normal_x[i])+" ")
    text_file.write ("\n")
    for i in range(len(normal_y)):
            text_file.write (str(normal_y[i])+" ")
    text_file.write ("\n")
    for i in range(len(triangles)):
        temp_triangle=triangles[i]
        for j in range(3):
            text_file.write (str(temp_triangle[j]+1)+" ")
        text_file.write ("\n")
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
def area(point):
    #v2 is the intersection point
    v1=point[1]-point[0]
    v2=point[2]-point[0]
    return abs(0.5*((v1.x*v2.y)-(v2.x*v1.y)))
def intersection_line_circle(u,v,radius,center_circle):
    u=u-center_circle
    v=v-center_circle
    m=float((u.y-v.y)/(u.x-v.x))
    b=u.y-m*u.x
    x1=(-2*m*b-sqrt((2*m*b)**2-4*(1+m**2)*(b**2-radius**2)))/2/(1+m**2)
    temp_vector=vector(x1,x1*m+b)
    if (abs(Length(u-temp_vector)+Length(v-temp_vector)-Length(u-v)))<=0.0001:
        return vector(x1,x1*m+b)+center_circle
    else:
        x1=(-2*m*b+sqrt((2*m*b)**2-4*(1+m**2)*(b**2-radius**2)))/2/(1+m**2)
        return vector(x1,x1*m+b)+center_circle
def find_volume_fraction(points,triangles,n,h,l,radius,radius_vector):
    count=0
    #initializing array
    volume_fraction=[]
    for i in range(len(triangles)):
            volume_fraction.append(0)

    #triangles all in shape
    for i in range(len(triangles)):
        temp_triangle=triangles[i]
        if (Length(points[temp_triangle[0]]-radius_vector))<=radius and (Length(points[temp_triangle[1]]-radius_vector))<=radius and (Length(points[temp_triangle[2]]-radius_vector))<=radius:
            volume_fraction[i]=1

    #triangles with one point in shape
    temp_approximate_triangle=[]
    for i in range(len(triangles)):
        temp_triangle=triangles[i]
        for j in range(3):
            if (Length(points[temp_triangle[j]]-radius_vector))<=radius:
                index=j
                count+=1
        if count==1:
            temp_approximate_triangle.append(points[temp_triangle[index]])
            for k in range (3):
                if k!=index:
                    temp_intersection=intersection_line_circle(points[temp_triangle[index]],points[temp_triangle[k]],radius,radius_vector)
                    temp_approximate_triangle.append(temp_intersection)
            temp_area=area(temp_approximate_triangle)
            temp_angle=acos(Dot(temp_approximate_triangle[1]-radius_vector,temp_approximate_triangle[2]-radius_vector)/Length(temp_approximate_triangle[2]-radius_vector)/Length(temp_approximate_triangle[1]-radius_vector))

            volume_fraction[i]=(temp_area+1/2*radius*radius*(temp_angle-sin(temp_angle)))/(l*l/2)
            if volume_fraction[i]>1:
                volume_fraction[i]=1
            temp_approximate_triangle=[]
        count=0

    #triangles with two point in shape
    for i in range(len(triangles)):
        temp_triangle=triangles[i]
        index=[]
        for j in range(3):
            if (Length(points[temp_triangle[j]]-radius_vector))<=radius:
                count+=1
                index.append(j)
        if count==2:
            volume_fraction[i]=0.75
            for p in range(3):
                if p!=index[0] and p!=index[1]:
                    index2=p
            temp_intersection2=[]
            for k in range(2):
                temp_intersection2.append(intersection_line_circle(points[temp_triangle[index2]],points[temp_triangle[index[k]]],radius,radius_vector))
            temp_triangle2=[temp_intersection2[0]]
            for k in range(2):
                temp_triangle2.append(points[temp_triangle[index[k]]])
            temp_triangle3=[]
            temp_triangle3.append(temp_intersection2[0])
            temp_triangle3.append(temp_intersection2[1])
            temp_triangle3.append(points[temp_triangle[index[1]]])
            temp_area2=area(temp_triangle2)+area(temp_triangle3)
            temp_angle=acos(Dot(temp_intersection2[0]-radius_vector,temp_intersection2[1]-radius_vector)/Length(temp_intersection2[0]-radius_vector)/Length(temp_intersection2[1]-radius_vector))
            volume_fraction[i]=(temp_area2+1/2*radius*radius*(temp_angle-sin(temp_angle)))/(l*l/2)
            if volume_fraction[i]>1:
                volume_fraction[i]=1

        count=0
    return volume_fraction
def find_normal(points,triangles,volume_fraction,radius_vector):
    normal_x=[]
    normal_y=[]
    for i in range(len(triangles)):
        normal_x.append(0)
        normal_y.append(0)
    count=0

    #triangles with one point in shape
    for i in range(len(triangles)):
        temp_triangle=triangles[i]
        intersection_points=[]

        for j in range(3):
            if (Length(points[temp_triangle[j]]-radius_vector))<=radius:
                index=j
                count+=1
        if (count==1 and volume_fraction[i]>0):
            angle=0
            count2=0
            for k in range (3):
                if k!=index:
                    temp_intersection=intersection_line_circle(points[temp_triangle[index]],points[temp_triangle[k]],radius,radius_vector)
                    if temp_intersection.x-radius_vector.x>0:
                        if temp_intersection.y-radius_vector.y>0:
                            temp_angle=atan((temp_intersection.y-radius_vector.y)/(temp_intersection.x-radius_vector.x))
                        else:
                            temp_angle=atan((temp_intersection.y-radius_vector.y)/(temp_intersection.x-radius_vector.x))+2*pi
                    else:
                        if temp_intersection.y-radius_vector.y>0:
                            temp_angle=atan((temp_intersection.y-radius_vector.y)/(temp_intersection.x-radius_vector.x))+pi
                        else:
                            temp_angle=atan((temp_intersection.y-radius_vector.y)/(temp_intersection.x-radius_vector.x))+pi
                    intersection_points.append(temp_intersection)
                    if count2==0:
                        angle=temp_angle
                        count2+=1
                    else:
                        if abs(angle-temp_angle)>pi:
                            angle=(angle+temp_angle-2*pi)/2
                        else:
                            angle=(angle+temp_angle)/2
            normal_x[i]=cos(angle)
            normal_y[i]=sin(angle)
        count=0

    #triangles with two point in shape
    for i in range(len(triangles)):
        temp_triangle=triangles[i]
        index=[]
        for j in range(3):
            if (Length(points[temp_triangle[j]]-radius_vector))<=radius:
                count+=1
                index.append(j)
        if count==2:
            volume_fraction[i]=0.75
            for p in range(3):
                if p!=index[0] and p!=index[1]:
                    index2=p
            temp_intersection2=[]
            for k in range(2):
                temp_intersection2.append(intersection_line_circle(points[temp_triangle[index2]],points[temp_triangle[index[k]]],radius,radius_vector))

                if temp_intersection2[k].x-radius_vector.x>0:
                    if temp_intersection2[k].y-radius_vector.y>0:
                         temp_angle=atan((temp_intersection2[k].y-radius_vector.y)/(temp_intersection2[k].x-radius_vector.x))
                    else:
                        temp_angle=atan((temp_intersection2[k].y-radius_vector.y)/(temp_intersection2[k].x-radius_vector.x))+2*pi
                else:
                    if temp_intersection2[k].y-radius_vector.y>0:
                         temp_angle=atan((temp_intersection2[k].y-radius_vector.y)/(temp_intersection2[k].x-radius_vector.x))+pi
                    else:
                         temp_angle=atan((temp_intersection2[k].y-radius_vector.y)/(temp_intersection2[k].x-radius_vector.x))+pi
                if k==0:
                    angle=temp_angle
                else:
                    if abs(angle-temp_angle)>pi:
                        angle=(angle+temp_angle-2*pi)/2
                    else:
                        angle=(angle+temp_angle)/2
            normal_x[i]=cos(angle)
            normal_y[i]=sin(angle)
        count=0
    return normal_x,normal_y
def find_center_of_circle(n,h,l):
    if n%2==0:
        if h%2==0:
            radius_vector=vector((n-1)*l/2,(h-1)*l/2-l/2)
        else:
            radius_vector=vector((n-1)*l/2,(h-1)*l/2)
    else:
        if h%2==0:
            radius_vector=vector((n-1)*l/2,(h-1)*l/2-l/2)
        else:
            radius_vector=vector((n-1)*l/2+l/2,(h-1)*l/2)
    print(radius_vector.x)
    print(radius_vector.y)
    return radius_vector
l=3 #length of triangle
h=5 #number of rows
n=5 #number of columns
radius=2 #radius of circle

points=create_points(h,n,l)
test=unstructured_mesh(points,l,h,n)
triangler=test.triangles()
radius_vector=find_center_of_circle(n,h,l)
volume_fraction=find_volume_fraction(points,triangler,n,h,l,radius,radius_vector)
normal_x,normal_y=find_normal(points,triangler,volume_fraction,radius_vector)
create_text(n,h,points,triangler,volume_fraction,normal_x,normal_y)





