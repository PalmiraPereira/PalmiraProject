__author__ = 'Palmira Pereira'
from math import *
import numpy as np
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
def Cross_product(u,v):
    #UcrossV
    return u.x*v.y-u.y*v.x

class edge(object):
    def __init__(self,points,point_list):
        self.point=[points[point_list[0]],points[point_list[1]]]
    def length(self):
        return abs(Length(self.point[0]-self.point[1]))
    def mid_point(self):
        return vector((self.point[1].x-self.point[0].x)*0.5,(self.point[1].y-self.point[0].y)*0.5)
class triangle(object):
    def __init__(self,points,point_list,height):
        self.point=[points[point_list[0]],points[point_list[1]],points[point_list[2]]]
        self.height=height
    def centroid (self):
        return vector((self.point[1].x+self.point[0].x+self.point[2].x)/3.0,(self.point[1].y+self.point[0].y+self.point[2].y)/3.0)
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
            points.append(vector(i*l+temp*l*0.5,j*l))
        if temp==0:
                temp=1
        else:
            temp=0
    return points
def create_text(n,h,points,triangles,volume_fraction,normal_x,normal_y,all_rectangle_points,normal_vof):
    text_file = open("triangle_upload_new.dat", "w")
    text_file.write("TITLE=\"TRIANGLE UPLOAD NEW\"\n")
    text_file.write("VARIABLES= \"X\",\"Y\",\"Volume Fraction\",\"U\",\"V\",\"CellNumber\"\n")
    text_file.write("ZONE\nDataPacking=Block\nZoneType=FETRIANGLE\n")
    text_file.write("N=")
    text_file.write(str(len(points)))
    text_file.write(" E=")
    text_file.write(str(n*2-2+(2*n-2)*(h-2)))
    text_file.write("\nVARLOCATION=([3-6]=CELLCENTERED)\n")
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
            text_file.write (str(normal_vof[i].x)+" ")
    text_file.write ("\n")
    for i in range(len(normal_y)):
            text_file.write (str(normal_vof[i].y)+" ")
    text_file.write ("\n")
    for i in range(len(normal_y)):
            text_file.write (str(i)+" ")
    text_file.write ("\n")
    for i in range(len(triangles)):
        temp_triangle=triangles[i]
        for j in range(3):
            text_file.write (str(temp_triangle[j]+1)+" ")
        text_file.write ("\n")


    ##extra zone for rectangle
    text_file.write("ZONE\nDataPacking=Block\nZoneType=FEQUADRILATERAL\n")
    text_file.write("N=")
    text_file.write(str(len(all_rectangle_points)*4))
    text_file.write(" E=")
    text_file.write(str(len(all_rectangle_points)))
    text_file.write("\nVARLOCATION=([3-6]=CELLCENTERED)\n")
    for i in all_rectangle_points:
        for j in range(4):
            text_file.write(str(i[j].x)+" ")
    text_file.write ("\n")
    for i in all_rectangle_points:
        for j in range(4):
            text_file.write(str(i[j].y)+" ")
    text_file.write ("\n")
    for i in range(len(all_rectangle_points)):
        text_file.write("4 ")
    text_file.write ("\n")
    for i in range(len(all_rectangle_points)):
        text_file.write("4 ")
    text_file.write ("\n")
    for i in range(len(all_rectangle_points)):
        text_file.write("4 ")
    text_file.write ("\n")
    for i in range(len(all_rectangle_points)):
        text_file.write("1 ")
    text_file.write ("\n")
    for i in range(len(all_rectangle_points)*4):
        if (i+1)%4==0:
            text_file.write(str(i+1))
            text_file.write ("\n")
        else:
            text_file.write(str(i+1)+" ")

    text_file.close()
def create_text_radius(approximate_radius_points_textfile):
    text_file = open("approximate_radius.dat", "w")

    for i in range(len(approximate_radius_points_textfile)):
            text_file.write (str(approximate_radius_points_textfile[i].x)+" "+str(approximate_radius_points_textfile[i].y)+"\n")

    text_file.close()
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
    if u.x-v.x!=0:
        m=float((u.y-v.y)/(u.x-v.x))
        b=u.y-m*u.x
        x1=(-2*m*b-sqrt((2*m*b)**2-4*(1+m**2)*(b**2-radius**2)))*0.5/(1+m**2)
        temp_vector=vector(x1,x1*m+b)
        if (abs(Length(u-temp_vector)+Length(v-temp_vector)-Length(u-v)))<=0.0001:
            return vector(x1,x1*m+b)+center_circle
        else:
            x1=(-2*m*b+sqrt((2*m*b)**2-4*(1+m**2)*(b**2-radius**2)))*0.5/(1+m**2)
            return vector(x1,x1*m+b)+center_circle
    else:
        b=u.x
        y1=sqrt(radius**2-b**2)
        temp_vector=vector(b,y1)
        if (abs(Length(u-temp_vector)+Length(v-temp_vector)-Length(u-v)))<=0.0001:
            return vector(b,y1)+center_circle
        else:
            return vector(b,-y1)+center_circle
def intersection_line_line(v1,v2,u1,u2):
    if u1.x==u2.x:
        b2=u1.x
        if v1.x==v2.x:
            return False
        else:
            m1=(v2.y-v1.y)/(v2.x-v1.x)
            b1=v2.y-m1*v2.x
            temp=vector(b2,m1*b2+b1)
            if abs(Length(v2-v1)-Length(v2-temp)-Length(v1-temp))<0.0000001 and abs(Length(u2-u1)-Length(u2-temp)-Length(u1-temp))<0.0000001:
                return temp
            else:
                return False
    elif v1.x==v2.x:
        b1=v1.x
        m2=(u2.y-u1.y)/(u2.x-u1.x)
        b2=u2.y-m2*u2.x
        temp=vector(b1,m2*b1+b2)
        if abs(Length(v2-v1)-Length(v2-temp)-Length(v1-temp))<0.0000001 and abs(Length(u2-u1)-Length(u2-temp)-Length(u1-temp))<0.0000001:
            return temp
        else:
            return False
    else:
        m1=(v2.y-v1.y)/(v2.x-v1.x)
        m2=(u2.y-u1.y)/(u2.x-u1.x)
        if m1==m2:
            return False
        b1=v2.y-m1*v2.x
        b2=u2.y-m2*u2.x
        x=(b2-b1)/(m1-m2)
        y=m1*x+b1
        temp=vector(x,y)
        if abs(Length(v2-v1)-Length(v2-temp)-Length(v1-temp))<0.0000001 and abs(Length(u2-u1)-Length(u2-temp)-Length(u1-temp))<0.0000001:
            return temp
        else:
            return False
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
            volume_fraction[i]=(temp_area+(0.5)*radius*radius*(temp_angle-sin(temp_angle)))/(float(l)*l/2)
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

            volume_fraction[i]=(temp_area2+0.5*radius*radius*(temp_angle-sin(temp_angle)))/(float(l)*l/2)
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
                            angle=(angle+temp_angle-2*pi)*0.5
                        else:
                            angle=(angle+temp_angle)*0.5
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
                    if temp_intersection2[k].x-radius_vector.x==0 and temp_intersection2[k].y-radius_vector.y<0:
                        temp_angle=pi*0.5+pi
                    elif temp_intersection2[k].x-radius_vector.x==0 and temp_intersection2[k].y-radius_vector.y>0:
                        temp_angle=pi*0.5
                    elif temp_intersection2[k].y-radius_vector.y>0:
                        temp_angle=atan((temp_intersection2[k].y-radius_vector.y)/(temp_intersection2[k].x-radius_vector.x))+pi
                    else:
                        temp_angle=atan((temp_intersection2[k].y-radius_vector.y)/(temp_intersection2[k].x-radius_vector.x))+pi
                if k==0:
                    angle=temp_angle
                else:
                    if abs(angle-temp_angle)>pi:
                        angle=(angle+temp_angle-2*pi)*0.5
                    else:
                        angle=(angle+temp_angle)*0.5
            normal_x[i]=cos(angle)
            normal_y[i]=sin(angle)
        count=0
    return normal_x,normal_y
def find_center_of_circle(n,h,l):
    if n%2==0:
        if h%2==0:
            radius_vector=vector((n-1)*l*0.5,(h-1)*l*0.5-l*0.5)
        else:
            radius_vector=vector((n-1)*l*0.5,(h-1)*l*0.5)
    else:
        if h%2==0:
            radius_vector=vector((n-1)*l*0.5,(h-1)*l*0.5-l*0.5)
        else:
            radius_vector=vector((n-1)*l*0.5+l*0.5,(h-1)*l*0.5)
    print(radius_vector.x)
    print(radius_vector.y)
    return radius_vector
def find_point_distance(point,angle,distance):
    return vector(cos(angle)*distance+point.x,sin(angle)*distance+point.y)
def find_height_function_vertices(length,width,normal_vector,bottom_point):
    #finding rectangle vertices
    rectangle_vertices=[]
    if normal_vector.y>0 and normal_vector.x==0:
        rectangle_vertices.append(vector(bottom_point.x-width*0.5,bottom_point.y))
        rectangle_vertices.append(vector(bottom_point.x-width*0.5,bottom_point.y+length))
        rectangle_vertices.append(vector(bottom_point.x+width*0.5,bottom_point.y+length))
        rectangle_vertices.append(vector(bottom_point.x+width*0.5,bottom_point.y))
    elif normal_vector.y<0 and normal_vector.x==0:
        rectangle_vertices.append(vector(bottom_point.x+width*0.5,bottom_point.y))
        rectangle_vertices.append(vector(bottom_point.x+width*0.5,bottom_point.y-length))
        rectangle_vertices.append(vector(bottom_point.x-width*0.5,bottom_point.y-length))
        rectangle_vertices.append(vector(bottom_point.x-width*0.5,bottom_point.y))
    elif normal_vector.x>0 and normal_vector.y==0:
        rectangle_vertices.append(vector(bottom_point.x,bottom_point.y+width*0.5))
        rectangle_vertices.append(vector(bottom_point.x+length,bottom_point.y+width*0.5))
        rectangle_vertices.append(vector(bottom_point.x+length,bottom_point.y-width*0.5))
        rectangle_vertices.append(vector(bottom_point.x,bottom_point.y-width*0.5))
    elif normal_vector.x>0 and normal_vector.y==0:
        rectangle_vertices.append(vector(bottom_point.x,bottom_point.y-width*0.5))
        rectangle_vertices.append(vector(bottom_point.x-length,bottom_point.y-width*0.5))
        rectangle_vertices.append(vector(bottom_point.x-length,bottom_point.y+width*0.5))
        rectangle_vertices.append(vector(bottom_point.x,bottom_point.y+width*0.5))
    elif normal_vector.x>0 and normal_vector.y>0:
        rectangle_vertices.append(find_point_distance(bottom_point,pi*0.5+atan(normal_vector.y/normal_vector.x),width*0.5))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[0],atan(normal_vector.y/normal_vector.x),length))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[1],-pi*0.5+atan(normal_vector.y/normal_vector.x),width))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[2],pi+atan(normal_vector.y/normal_vector.x),length))
    elif normal_vector.x<0 and normal_vector.y>0:
        rectangle_vertices.append(find_point_distance(bottom_point,3*0.5*pi-atan(-normal_vector.y/normal_vector.x),width*0.5))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[0],pi-atan(-normal_vector.y/normal_vector.x),length))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[1],pi*0.5-atan(-normal_vector.y/normal_vector.x),width))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[2],-atan(-normal_vector.y/normal_vector.x),length))
    elif normal_vector.x<0 and normal_vector.y<0:
        rectangle_vertices.append(find_point_distance(bottom_point,pi*3*0.5+atan(normal_vector.y/normal_vector.x),width*0.5))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[0],pi+atan(normal_vector.y/normal_vector.x),length))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[1],pi*0.5+atan(normal_vector.y/normal_vector.x),width))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[2],atan(normal_vector.y/normal_vector.x),length))
    elif normal_vector.x>0 and normal_vector.y<0:
        rectangle_vertices.append(find_point_distance(bottom_point,pi*3*0.5-atan(-normal_vector.y/normal_vector.x),width*0.5))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[0],-atan(-normal_vector.y/normal_vector.x),length))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[1],pi*0.5-atan(-normal_vector.y/normal_vector.x),width))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[2],pi-atan(-normal_vector.y/normal_vector.x),length))
    return rectangle_vertices
def find_area_height_function(rectangle_vertices,points,triangles):

    rectangle_vertices.append(rectangle_vertices[0])
    list_of_inside_triangles=[]
    area_inside_rectangle=[]

    for i in range(len(triangles)):
        area_inside_rectangle.append(0)

    for i in range(len(triangles)):
        required_points=[]
        i2=triangles[i]
        i2.append(i2[0])
        temp_intersection=[]
        for j in range(len(rectangle_vertices)-1):
            for k in range(len(i2)-1):
                if intersection_line_line(points[i2[k]],points[i2[k+1]],rectangle_vertices[j],rectangle_vertices[j+1])!=False:
                    list_of_inside_triangles.append(i2)
                    temp_intersection.append(intersection_line_line(points[i2[k]],points[i2[k+1]],rectangle_vertices[j],rectangle_vertices[j+1]))
                    required_points.append(intersection_line_line(points[i2[k]],points[i2[k+1]],rectangle_vertices[j],rectangle_vertices[j+1]))

        temp=[]
        temp_triangle=triangles[i]

        for j in range(len(temp_triangle)-1):
            if (0<Dot(points[temp_triangle[j]]-rectangle_vertices[1],rectangle_vertices[2]-rectangle_vertices[1])<Dot(rectangle_vertices[2]-rectangle_vertices[1],rectangle_vertices[2]-rectangle_vertices[1])) and (0<Dot(points[temp_triangle[j]]-rectangle_vertices[1],rectangle_vertices[0]-rectangle_vertices[1])<Dot(rectangle_vertices[0]-rectangle_vertices[1],rectangle_vertices[0]-rectangle_vertices[1])):
                temp.append(points[temp_triangle[j]])
                required_points.append(points[temp_triangle[j]])
        rec=[]
        for j in range(len(rectangle_vertices)-1):
                total_area=area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])
                area1=area([rectangle_vertices[j],points[temp_triangle[1]],points[temp_triangle[2]]])
                area2=area([rectangle_vertices[j],points[temp_triangle[0]],points[temp_triangle[2]]])
                area3=area([rectangle_vertices[j],points[temp_triangle[0]],points[temp_triangle[1]]])
                if abs(area1+area2+area3-total_area)<0.000001:
                    rec.append(rectangle_vertices[j])
                    required_points.append(rectangle_vertices[j])
        for j in range(len(rectangle_vertices)-1):
            for k in range(len(temp_triangle)-1):
                if abs(Length(rectangle_vertices[j]-points[temp_triangle[k]])+Length(rectangle_vertices[j]-points[temp_triangle[k+1]])-Length(points[temp_triangle[k+1]]-points[temp_triangle[k]]))<0.00000001:
                    required_points.append(rectangle_vertices[j])

        distance=0
        index=-1
        for j in range(len(required_points)):
            if required_points[j].x>distance:
                distance=required_points[j].x
                index=j
        if index!=-1:

            required_points_sorted=sort_counterclockwise(required_points[index],required_points)

            area_inside_rectangle[i]=area_polygon(required_points_sorted[0],required_points_sorted)

    total=0
    for i in area_inside_rectangle:
        total=total+i
    print (total)
    return (area_inside_rectangle)
def find_adj_cell(triangles):
    adj_cell=[]
    for i in range(len(triangles)):
        temp_adj_cell=[-1,-1,-1]
        for k in range(len(triangles)):
            if triangles[i]!=triangles[k]:
                temp_triangle=triangles[i]
                count=0
                j=[temp_triangle[0],temp_triangle[1]]
                for p in triangles[k]:
                    if p==j[0]:
                        count=count+1
                    elif p==j[1]:
                        count=count+1
                if count==2:
                    temp_adj_cell[0]=k
                count=0
                j=[temp_triangle[1],temp_triangle[2]]
                for p in triangles[k]:
                    if p==j[0]:
                        count=count+1
                    elif p==j[1]:
                        count=count+1
                if count==2:
                    temp_adj_cell[1]=k
                count=0
                j=[temp_triangle[0],temp_triangle[2]]
                for p in triangles[k]:
                    if p==j[0]:
                        count=count+1
                    elif p==j[1]:
                        count=count+1
                if count==2:
                    temp_adj_cell[2]=k
        adj_cell.append(temp_adj_cell)
    return (adj_cell)
def find_height(volume_fraction,points,test,normal_x,normal_y,h,l,circle_center):

    #rectangle parameters
    length=8
    width=0.9
    spacing=0.0
    totalcic=0
    for w in range(len(volume_fraction)):
        if volume_fraction[w]!=0 :
            totalcic=totalcic+volume_fraction[w]
    print(totalcic*l*l*0.5/radius/radius/pi)
    approximate_radius_points_textfile=[]
    approximate_radius_points=[]
    all_rectangle_points=[]
    for w in range(len(volume_fraction)):
        approximate_radius_point=vector(-1,-1)
        approximate_radius_point2=vector(-1,-1)
        approximate_radius_point3=vector(-1,-1)
        if volume_fraction[w]!=1 and volume_fraction[w]!=0:

            normal=vector(normal_x[w],normal_y[w])
            triangler=test.triangles()
            triangler2=triangle(points,test.triangles()[w],h)
            centroid=triangler2.centroid()

            if normal.x==0 and normal.y>0:
                angle=pi*0.5
            elif normal.x==0 and normal.y<0:
                angle=pi*0.5*3
            elif normal.x<0 and normal.y<0:
                angle=atan(normal.y/normal.x)+pi
            elif normal.x<0 and normal.y>0:
                angle=atan(normal.y/normal.x)+pi
            else:
                angle=atan(normal.y/normal.x)

            angle=angle+pi
            bottom_point=find_point_distance(centroid,angle,length*0.5)

            rectangle_vertices=find_height_function_vertices(length,width,normal,bottom_point)
            all_rectangle_points.append(rectangle_vertices)
            area_inside=find_area_height_function(rectangle_vertices,points,triangler)

            height=0
            for k in range(len(volume_fraction)):
                height=height+volume_fraction[k]*area_inside[k]
            height=height/width
            appr_circl=find_point_distance(bottom_point,angle-pi,height)
            approximate_radius_point=appr_circl

            bottom_point2=find_point_distance(bottom_point,angle-pi/2,width+spacing)
            rectangle_vertices=find_height_function_vertices(length,width,normal,bottom_point2)
            all_rectangle_points.append(rectangle_vertices)
            area_inside=find_area_height_function(rectangle_vertices,points,triangler)
            height=0
            for k in range(len(volume_fraction)):
                height=height+volume_fraction[k]*area_inside[k]
            height=height/width
            appr_circl=find_point_distance(bottom_point2,angle-pi,height)
            approximate_radius_point2=appr_circl


            bottom_point3=find_point_distance(bottom_point,angle+pi/2,width+spacing)
            rectangle_vertices=find_height_function_vertices(length,width,normal,bottom_point3)
            all_rectangle_points.append(rectangle_vertices)
            area_inside=find_area_height_function(rectangle_vertices,points,triangler)
            height=0
            for k in range(len(volume_fraction)):
                height=height+volume_fraction[k]*area_inside[k]
            height=height/width
            appr_circl=find_point_distance(bottom_point3,angle-pi,height)
            approximate_radius_point3=appr_circl
        approximate_radius_points.append([approximate_radius_point,approximate_radius_point2,approximate_radius_point3])

        if approximate_radius_point.x!=-1 and approximate_radius_point.y!=-1:
            approximate_radius_points_textfile.append(approximate_radius_point)
            approximate_radius_points_textfile.append(approximate_radius_point2)
            approximate_radius_points_textfile.append(approximate_radius_point3)


    create_text_radius(approximate_radius_points_textfile)




    #print(area_inside)

    return approximate_radius_points,all_rectangle_points
def sort_counterclockwise(middle,points_around):

    points_around_polar=[]
    for i in range(len(points_around)):
        points_around[i]=points_around[i]-middle

    for i in points_around:
        if i.x==0 and i.y>0:
            temp_angle=pi*0.5
            temp_radius=i.y
        elif i.x==0 and i.y==0:
            temp_angle=0
            temp_radius=0
        elif i.x==0 and i.y<0:
            temp_angle=pi*3*0.5
            temp_radius=-i.y
        elif i.x>0 and i.y==0:
            temp_angle=0
            temp_radius=i.x
        elif i.x<0 and i.y==0:
            temp_angle=pi
            temp_radius=-i.x
        elif i.x>0 and i.y>0:
            temp_angle=atan(i.y/i.x)
            temp_radius=Length(i)
        elif i.x<0 and i.y>0:

            temp_angle=pi-atan(-i.y/i.x)
            temp_radius=Length(i)
        elif i.x<0 and i.y<0:
            temp_angle=pi+atan(i.y/i.x)
            temp_radius=Length(i)
        else:
            temp_angle=2*pi-atan(-i.y/i.x)
            temp_radius=Length(i)
        points_around_polar.append([temp_angle,temp_radius])
    index=[]
    temp_index=0
    temp_closest=[[2*pi,5]]
    for j in points_around_polar:
        temp_closest[0]=2*pi
        for i in range(len(points_around_polar)):
            temp_point=points_around_polar[i]
            if i not in index:
                if temp_point[0]<temp_closest[0]:
                    temp_closest[0]=temp_point[0]
                    temp_index=i
        index.append(temp_index)
    points_around_sorted=[]
    points_around_sorted.append(middle)
    for i in index:
        if Length(points_around[i])>0.00000001:
            points_around_sorted.append(points_around[i]+middle)

    return(points_around_sorted)
def area_polygon(middle,sorted):
    total_area=0
    for i in range(len(sorted)-1):
        #print(middle.x)
        #print(middle.y)
        #print(sorted[i].x)
        #print(sorted[i].y)
        #print(sorted[i+1].x)
        #print(sorted[i+1].y)

        total_area=total_area+area([middle,sorted[i],sorted[i+1]])
    return (total_area)
def curvature(volume_fraction,approximate_radius_points,test,h,points,radius):
    parabolic_approximation_coefficients=[]
    singular_matrix_index=[]
    for k in range(len(approximate_radius_points)):
        j=approximate_radius_points[k]
        x=np.matrix([[0]])
        if j[0].x!=-1 and j[0].y!=-1:
            a=np.array([[j[0].x**2,j[0].x,1],[j[1].x**2,j[1].x,1],[j[2].x**2,j[2].x,1]])
            if np.linalg.det(a)!=0:
                b=np.array([[j[0].y],[j[1].y],[j[2].y]])
                x=np.linalg.solve(a,b)
            else:
                a=np.array([[j[0].y**2,j[0].y,1],[j[1].y**2,j[1].y,1],[j[2].y**2,j[2].y,1]])
                b=np.array([[j[0].x],[j[1].x],[j[2].x]])
                x=np.linalg.solve(a,b)
                singular_matrix_index.append(k)
                print("singular matrix")
        parabolic_approximation_coefficients.append(x)
        list_centroid=[]

    for w in range(len(volume_fraction)):
        triangler2=triangle(points,test.triangles()[w],h)
        list_centroid.append(triangler2.centroid())
    print(singular_matrix_index)
    curvature=[]
    for w in range(len(list_centroid)):
        temp_parabolic_approximation_coefficients=parabolic_approximation_coefficients[w]
        if len(temp_parabolic_approximation_coefficients)!=1:
            if w not in singular_matrix_index:
                curvature.append(2*temp_parabolic_approximation_coefficients[0][0]/(1+(2*temp_parabolic_approximation_coefficients[0][0]*list_centroid[w].x+temp_parabolic_approximation_coefficients[1][0])**2)**(1.5))
    error_curvature=[]
    for w in curvature:
        error_curvature.append(abs(1/float(radius)-abs(w)))
    print(curvature)
    print(error_curvature)
    print(max(error_curvature))
    return (list_centroid,curvature)
def find_surface_normal(points,triangles,list_centroid):
    surface_normal=[]
    for j in range(len(triangles)):
        w=triangles[j]
        temp_surface_normal=[]
        temp_surface_normal.append(vector(-(points[w[1]].y-points[w[0]].y),points[w[1]].x-points[w[0]].x)*(1/(Length(vector(-(points[w[1]].y-points[w[0]].y),points[w[1]].x-points[w[0]].x)))))
        if (Dot(vector(points[w[1]].x+points[w[0]].x,points[w[1]].y+points[w[0]].y)*0.5-list_centroid[j],vector(-(points[w[1]].y-points[w[0]].y),points[w[1]].x-points[w[0]].x)*(1/(Length(vector(-(points[w[1]].y-points[w[0]].y),points[w[1]].x-points[w[0]].x))))))<0:
            temp_surface_normal[0]=temp_surface_normal[0]*-1
        temp_surface_normal.append(vector(-(points[w[1]].y-points[w[2]].y),points[w[1]].x-points[w[2]].x)*(1/(Length(vector(-(points[w[1]].y-points[w[2]].y),points[w[1]].x-points[w[2]].x)))))
        if (Dot(vector(points[w[1]].x+points[w[2]].x,points[w[1]].y+points[w[2]].y)*0.5-list_centroid[j],vector(-(points[w[1]].y-points[w[2]].y),points[w[1]].x-points[w[2]].x)*(1/(Length(vector(-(points[w[1]].y-points[w[2]].y),points[w[1]].x-points[w[2]].x))))))<0:
            temp_surface_normal[1]=temp_surface_normal[1]*-1
        temp_surface_normal.append(vector(-(points[w[0]].y-points[w[2]].y),points[w[0]].x-points[w[2]].x)*(1/(Length(vector(-(points[w[0]].y-points[w[2]].y),points[w[0]].x-points[w[2]].x)))))
        if (Dot(vector(points[w[0]].x+points[w[2]].x,points[w[0]].y+points[w[2]].y)*0.5-list_centroid[j],vector(-(points[w[0]].y-points[w[2]].y),points[w[0]].x-points[w[2]].x)*(1/(Length(vector(-(points[w[0]].y-points[w[2]].y),points[w[0]].x-points[w[2]].x))))))<0:
            temp_surface_normal[2]=temp_surface_normal[2]*-1
        surface_normal.append(temp_surface_normal)
    #for w in surface_normal:
        #for j in w:
            #print(j.x)
            #print(j.y)
        #print()
    return(surface_normal)
def find_function_f_interpolation_colour_function(volume_fraction,triangles,adj_cell,points):
    function_f=[]
    for w in range(len(triangles)):
        temp_function_f=[]
        temp_triangle=triangles[w]
        temp_adj_cell=adj_cell[w]
        area_o=area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])
        for k in range(len(temp_adj_cell)):
            if temp_adj_cell[k]!=-1:
                temp_triangle_NB=triangles[temp_adj_cell[k]]
                area_NB=area([points[temp_triangle_NB[0]],points[temp_triangle_NB[1]],points[temp_triangle_NB[2]]])
                temp_function_f.append(area_NB/(area_NB+area_o)*volume_fraction[w]+area_o/(area_NB+area_o)*volume_fraction[temp_adj_cell[k]])
            else:
                temp_function_f.append(-1)
        function_f.append(temp_function_f)
    #for w in range(len(function_f)):
        #print(w)
        #print(function_f[w])
    return(function_f)
def find_normal_vof(function_f,surface_normal,points,triangles,volume_fraction,normal_x,normal_y):
    gradient_f=[]
    normal=[]
    for w in range(len(volume_fraction)):
        #print(w)
        temp_triangle=triangles[w]
        temp_function_f=function_f[w]
        if temp_function_f[0]!=-1 and temp_function_f[1]!=-1 and temp_function_f[2]!=-1:

            temp_surface_normal=surface_normal[w]
            temp_surface_normal2=[]
            for k in range(len(surface_normal[w])):
                temp_surface_normal2.append(temp_surface_normal[k]*temp_function_f[k])
                #print(temp_surface_normal[k].x)
                #print(temp_surface_normal[k].y)
                #print(temp_function_f[k])
                #print((temp_surface_normal[k]*temp_function_f[k]).x)
                #print((temp_surface_normal[k]*temp_function_f[k]).y)
                #print()
            gradient_f.append((temp_surface_normal2[0]+temp_surface_normal2[1]+temp_surface_normal2[2])*(1/area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])))
            if Length(gradient_f[w])!=0:
                normal.append(gradient_f[w]*(-1/Length(gradient_f[w])))
            else:
                normal.append(vector(0,0))
        else:
            normal.append(vector(0,0))
            gradient_f.append([])
        #print(w)
        #if normal[w]!=[]:
            #print(normal[w].x)
            #print(normal[w].y)
        #print()
    #for w in range(len(normal_x)):
        #if normal[w]!=[] and normal[w].x==0 and normal[w].y!=0:
            #print(w)
            #print(normal[w].x)
            #print(normal[w].y)
            #print(normal_x[w])
            #print(normal_y[w])
            #print()

    return(normal)
def find_function_f_interpolation_normal(normal_vof,triangles,adj_cell,points):
    function_f=[]
    print(adj_cell)
    for w in range(len(triangles)):
        temp_function_f=[]
        temp_triangle=triangles[w]
        temp_adj_cell=adj_cell[w]
        area_o=area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])
        for k in range(len(temp_adj_cell)):
            if temp_adj_cell[k]!=-1:
                temp_triangle_NB=triangles[temp_adj_cell[k]]
                area_NB=area([points[temp_triangle_NB[0]],points[temp_triangle_NB[1]],points[temp_triangle_NB[2]]])
                temp_function_f.append((normal_vof[w]*(area_NB/(area_NB+area_o)))+(normal_vof[temp_adj_cell[k]]*(area_o/(area_NB+area_o))))
            else:
                temp_function_f.append(-1)

        function_f.append(temp_function_f)
    #for w in range(len(function_f)):
        #print(w)
        #temp=function_f[w]
        #for k in temp:
            #if k!=-1:
                #print(k.x)
                #print(k.y)
        #print()
    return(function_f)
def find_curvature_vof(function_f_normal_vof,surface_normal,points,triangles,volume_fraction):
    gradient_f=[]
    for w in range(len(volume_fraction)):
        #print(w)
        temp_triangle=triangles[w]
        temp_function_f=function_f_normal_vof[w]
        if volume_fraction[w]!=0 and volume_fraction[w]!=1:

            temp_surface_normal=surface_normal[w]
            temp_surface_normal2=[]
            for k in range(len(surface_normal[w])):
                temp_surface_normal2.append(Dot(temp_surface_normal[k],temp_function_f[k]))
                #print(temp_surface_normal[k].x)
                #print(temp_surface_normal[k].y)
                #print(temp_function_f[k].x)
                #print(temp_function_f[k].y)
                #print((Dot(temp_surface_normal[k],temp_function_f[k])))
                #print()
            gradient_f.append((temp_surface_normal2[0]+temp_surface_normal2[1]+temp_surface_normal2[2])*(-1/area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])))
        else:
            gradient_f.append([])
        #print(w)
        #if gradient_f[w]!=[]:
            #print(gradient_f[w])
        #print()
    #for w in range(len(normal_x)):
        #if normal[w]!=[] and normal[w].x==0 and normal[w].y!=0:
            #print(w)
            #print(normal[w].x)
            #print(normal[w].y)
            #print(normal_x[w])
            #print(normal_y[w])
            #print()
    return(gradient_f)
def create_text_curvature(curvature_height):
    text_file = open("curvature_height.dat", "w")
    for i in range(len(curvature_height)):
            text_file.write (str(curvature_height[i]))
            text_file.write ("\n")

#mesh parameters
l=2.5 #length of triangle
h=20 #number of rows
n=20 #number of columns
#circle parameters
radius=8 #radius of circle
circle_center=find_center_of_circle(n,h,l)

points=create_points(h,n,l)
test=unstructured_mesh(points,l,h,n)
triangler=test.triangles()
volume_fraction=find_volume_fraction(points,triangler,n,h,l,radius,circle_center)
normal_x,normal_y=find_normal(points,triangler,volume_fraction,circle_center)
approximate_radius_points,all_rectangle_points=find_height(volume_fraction,points,test,normal_x,normal_y,h,l,circle_center)


list_centroid,curvature_height=curvature(volume_fraction,approximate_radius_points,test,h,points,radius)


adj_cell=find_adj_cell(triangler)
surface_normal=find_surface_normal(points,triangler,list_centroid)
function_f=find_function_f_interpolation_colour_function(volume_fraction,triangler,adj_cell,points)
normal_vof=find_normal_vof(function_f,surface_normal,points,triangler,volume_fraction,normal_x,normal_y)
create_text(n,h,points,triangler,volume_fraction,normal_x,normal_y,all_rectangle_points,normal_vof)
function_f_normal_vof=find_function_f_interpolation_normal(normal_vof,triangler,adj_cell,points)
curvature_vof=find_curvature_vof(function_f_normal_vof,surface_normal,points,triangler,volume_fraction)
create_text_curvature(curvature_height)
