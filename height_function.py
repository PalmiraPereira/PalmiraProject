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
def Cross_product(u,v):
    #UcrossV
    return u.x*v.y-u.y*v.x

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
def create_text(n,h,points,triangles,volume_fraction,normal_x,normal_y,rectangle_vertices):
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


    ##extra zone for rectangle
    text_file.write("ZONE\nDataPacking=Block\nZoneType=FEQUADRILATERAL\n")
    text_file.write("N=")
    text_file.write(str(4))
    text_file.write(" E=")
    text_file.write(str(1))
    text_file.write("\nVARLOCATION=([3-5]=CELLCENTERED)\n")
    for i in range(4):
        text_file.write(str(rectangle_vertices[i].x)+" ")
    text_file.write ("\n")
    for i in range(4):
        text_file.write(str(rectangle_vertices[i].y)+" ")
    text_file.write ("\n1\n1\n1\n1 2 3 4")
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
def find_point_distance(point,angle,distance):
    return vector(cos(angle)*distance+point.x,sin(angle)*distance+point.y)
def find_height_function_vertices(length,width,normal_vector,bottom_point):
    #finding rectangle vertices
    rectangle_vertices=[]
    if normal_vector.y>0 and normal_vector.x==0:
        rectangle_vertices.append(vector(bottom_point.x-width/2,bottom_point.y))
        rectangle_vertices.append(vector(bottom_point.x-width/2,bottom_point.y+length))
        rectangle_vertices.append(vector(bottom_point.x+width/2,bottom_point.y+length))
        rectangle_vertices.append(vector(bottom_point.x+width/2,bottom_point.y))
    elif normal_vector.y<0 and normal_vector.x==0:
        rectangle_vertices.append(vector(bottom_point.x+width/2,bottom_point.y))
        rectangle_vertices.append(vector(bottom_point.x+width/2,bottom_point.y-length))
        rectangle_vertices.append(vector(bottom_point.x-width/2,bottom_point.y-length))
        rectangle_vertices.append(vector(bottom_point.x-width/2,bottom_point.y))
    elif normal_vector.x>0 and normal_vector.y==0:
        rectangle_vertices.append(vector(bottom_point.x,bottom_point.y+width/2))
        rectangle_vertices.append(vector(bottom_point.x+length,bottom_point.y+width/2))
        rectangle_vertices.append(vector(bottom_point.x+length,bottom_point.y-width/2))
        rectangle_vertices.append(vector(bottom_point.x,bottom_point.y-width/2))
    elif normal_vector.x>0 and normal_vector.y==0:
        rectangle_vertices.append(vector(bottom_point.x,bottom_point.y-width/2))
        rectangle_vertices.append(vector(bottom_point.x-length,bottom_point.y-width/2))
        rectangle_vertices.append(vector(bottom_point.x-length,bottom_point.y+width/2))
        rectangle_vertices.append(vector(bottom_point.x,bottom_point.y+width/2))
    elif normal_vector.x>0 and normal_vector.y>0:
        rectangle_vertices.append(find_point_distance(bottom_point,pi/2+atan(normal_vector.y/normal_vector.x),width/2))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[0],atan(normal_vector.y/normal_vector.x),length))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[1],-pi/2+atan(normal_vector.y/normal_vector.x),width))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[2],pi+atan(normal_vector.y/normal_vector.x),length))
    elif normal_vector.x<0 and normal_vector.y>0:
        rectangle_vertices.append(find_point_distance(bottom_point,3/2*pi-atan(-normal_vector.y/normal_vector.x),width/2))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[0],pi-atan(-normal_vector.y/normal_vector.x),length))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[1],pi/2-atan(-normal_vector.y/normal_vector.x),width))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[2],-atan(-normal_vector.y/normal_vector.x),length))
    elif normal_vector.x<0 and normal_vector.y<0:
        rectangle_vertices.append(find_point_distance(bottom_point,pi*3/2+atan(normal_vector.y/normal_vector.x),width/2))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[0],pi+atan(normal_vector.y/normal_vector.x),length))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[1],pi/2+atan(normal_vector.y/normal_vector.x),width))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[2],atan(normal_vector.y/normal_vector.x),length))
    elif normal_vector.x>0 and normal_vector.y<0:
        rectangle_vertices.append(find_point_distance(bottom_point,atan(-normal_vector.y/normal_vector.x),width/2))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[0],-atan(-normal_vector.y/normal_vector.x),length))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[1],pi*3/2-atan(-normal_vector.y/normal_vector.x),width))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[2],pi-atan(-normal_vector.y/normal_vector.x),length))
    return rectangle_vertices
def find_height_function(rectangle_vertices,points,triangles):
    rectangle_vertices.append(rectangle_vertices[0])
    list_of_inside_triangles=[]
    list_of_intersections=[]
    output = []
    area_inside_rectangle=[]
    for i in range(len(triangles)):
        area_inside_rectangle.append(0)

    #finding intersection points
    for i in triangles:
        i.append(i[0])
        temp_intersection=[]
        for j in range(len(rectangle_vertices)-1):
            for k in range(len(i)-1):
                if intersection_line_line(points[i[k]],points[i[k+1]],rectangle_vertices[j],rectangle_vertices[j+1])!=False:
                    list_of_inside_triangles.append(i)
                    temp_intersection.append(intersection_line_line(points[i[k]],points[i[k+1]],rectangle_vertices[j],rectangle_vertices[j+1]))
        list_of_intersections.append(temp_intersection)
    for x in list_of_inside_triangles:
        if x not in output:
            output.append(x)
    list_of_inside_triangles=output

    #finding nodes inside rectangle
    list_of_one_node_inside=[]
    inside_points=[]
    for i in range(len(triangles)):
        count=0
        temp=[]
        temp_triangle=triangles[i]
        for j in range(len(temp_triangle)-1):
            if (0<Dot(points[temp_triangle[j]]-rectangle_vertices[1],rectangle_vertices[2]-rectangle_vertices[1])<Dot(rectangle_vertices[2]-rectangle_vertices[1],rectangle_vertices[2]-rectangle_vertices[1])) and (0<Dot(points[temp_triangle[j]]-rectangle_vertices[1],rectangle_vertices[0]-rectangle_vertices[1])<Dot(rectangle_vertices[0]-rectangle_vertices[1],rectangle_vertices[0]-rectangle_vertices[1])):
                temp.append(points[temp_triangle[j]])
                count+=1
        if count==1:
            list_of_one_node_inside.append(i)
        inside_points.append(temp)
        #3 nodes inside rectangle
        if count==3:
            area_inside_rectangle[i]=area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])
        #2 nodes inside rectangle
        elif count==2:

            count2=0
            for j in range(len(rectangle_vertices)-1):
                total_area=area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])
                area1=area([rectangle_vertices[j],points[temp_triangle[1]],points[temp_triangle[2]]])
                area2=area([rectangle_vertices[j],points[temp_triangle[0]],points[temp_triangle[2]]])
                area3=area([rectangle_vertices[j],points[temp_triangle[0]],points[temp_triangle[1]]])
                if abs(area1+area2+area3-total_area)<0.000001:
                    count2=1
                    inside_rec_point=rectangle_vertices[j]
            for j in range(len(temp_triangle)-1):
                if points[temp_triangle[j]]!=temp[0] and points[temp_triangle[j]]!=temp[1]:
                    temp.append(points[temp_triangle[j]])
            temp3=[]
            for k in range(len(temp)-1):
                temp3.append(temp[k])
            temp2=list_of_intersections[i]

            temp3.append(temp2[0])

            area_inside_rectangle[i]=area(temp3)
            temp3=[]
            for j in temp2:
                temp3.append(j)
            if abs(area([temp[0],temp[1],temp2[0]])+area([temp2[0],temp2[1],temp[2]])+area([temp2[0],temp2[1],temp[1]])-area([temp[0],temp[1],temp[2]]))<0.0000000001:
                temp3.append(temp[1])
            else:
                temp3.append(temp[0])
            area_inside_rectangle[i]=area_inside_rectangle[i]+area(temp3)
            if len(temp2)==4:
                temp3=[]
                temp3.append(temp[2])
                for k in temp2:
                    if (abs(temp[0].x-k.x)>0.00001 or abs(temp[0].y-k.y)>0.00001) and (abs(temp[1].x-k.x)>0.00001 or abs(temp[1].y-k.y)>0.00001) :
                        temp3.append(k)
                area_inside_rectangle[i]=area(temp)-area(temp3)

            if len(temp2)==3:
                temp3=[]
                for k in temp2:
                    if abs(k.x-temp[0].x)>0.001 and abs(k.x-temp[0].x)>0.001:
                        temp3.append(k)
                temp3.append(temp[0])
                temp3.append(temp[1])
                area_inside_rectangle[i]=area(temp3)
            if count2==1:
                temp3[2]=inside_rec_point
                area_inside_rectangle[i]=area_inside_rectangle[i]+area(temp3)
        elif count==0:


            temp3=[]

            if list_of_intersections[i]!=[]:

                if len(list_of_intersections[i])==4:
                    distance=length
                    for k in rectangle_vertices:
                        for j in list_of_intersections[i]:
                            if Length(k-j)<distance:
                                node=k
                                distance=Length(k-j)
                    distance=0
                    far_points=[]
                    intersection3=list_of_intersections[i]
                    for k in intersection3:
                        if Length(k-node)>distance:
                            distance=Length(k-node)
                            temp5=k
                    far_points.append(temp5)
                    distance=0
                    for k in intersection3:
                        if k!=far_points[0]:
                            if Length(k-node)>distance:
                                distance=Length(k-node)
                                temp5=k
                    far_points.append(temp5)
                    area_inside_rectangle[i]=area([far_points[0],far_points[1],node])
                    for k in intersection3:
                        if k!=far_points[0] and k!=far_points[1]:
                            far_points.append(k)
                    area_inside_rectangle[i]=area_inside_rectangle[i]-area([far_points[2],far_points[3],node])
                    if area_inside_rectangle[i]==0:
                        temp6=list_of_intersections[i]
                        temp3.append(temp6[0])
                        if temp3[0].x!=temp6[1].x or temp3[0].y!=temp6[1].y:
                            temp3.append(temp6[1])
                        if len(temp3)==2:
                            if (temp3[0].x==temp6[2].x and temp3[0].y==temp6[2].y) or (temp3[1].x!=temp6[2].x and temp3[1].y!=temp6[2].y):
                                temp3.append(temp6[3])
                            else:
                                temp3.append(temp6[2])

                        else:
                            temp3.append(temp6[2])
                            temp3.append((temp6[3]))
                        area_inside_rectangle[i]=area(temp3)
                else:

                    temp_intersection=list_of_intersections[i]
                    if abs(temp_intersection[0].x-temp_intersection[1].x)<0.00001 and abs(temp_intersection[0].y-temp_intersection[1].y)<0.00001:
                        area_inside_rectangle[i]=0

                    else:
                        for k in range(len(rectangle_vertices)-1):
                            total_area=area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])
                            area1=area([rectangle_vertices[k],points[temp_triangle[1]],points[temp_triangle[2]]])
                            area2=area([rectangle_vertices[k],points[temp_triangle[0]],points[temp_triangle[2]]])
                            area3=area([rectangle_vertices[k],points[temp_triangle[0]],points[temp_triangle[1]]])
                            if abs(area1+area2+area3-total_area)<0.000001:
                                temp2=rectangle_vertices[k]
                        for k in list_of_intersections[i]:
                            temp3.append(k)
                        temp3.append(temp2)
                        if len(temp3)==4:
                           for j in range(2):
                               if abs(temp3[0].x-temp3[j+1].x)<0.0001 and abs(temp3[0].y-temp3[j+1].y)<0.0001:
                                   temp3.pop(j+1)
                           if len(temp3)==4:
                               for k in range(1):
                                   if abs(temp3[1].x-temp3[k+2].x)<0.0001 and abs(temp3[1].y-temp3[k+2].y)<0.0001:
                                       temp3.pop(k+2)
                               if len(temp3)==4:
                                   temp3.pop(3)

                        area_inside_rectangle[i]=area(temp3)
    for i in list_of_one_node_inside:

        temp_triangle=triangles[i]
        count2=0
        for j in range(len(rectangle_vertices)-1):
            total_area=area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])
            area1=area([rectangle_vertices[j],points[temp_triangle[1]],points[temp_triangle[2]]])
            area2=area([rectangle_vertices[j],points[temp_triangle[0]],points[temp_triangle[2]]])
            area3=area([rectangle_vertices[j],points[temp_triangle[0]],points[temp_triangle[1]]])
            if abs(area1+area2+area3-total_area)<0.000001:
                count2=1
                inside_rec_point=rectangle_vertices[j]
        #case 2
        if count2==0:
            temp4=[]
            for k in list_of_intersections[i]:
                temp4.append(k)
            temp2=inside_points[i]
            temp4.append(temp2[0])
            #case 1
            if len(temp4)==3:
                area_inside_rectangle[i]=area(temp4)
            #case 3
            else:
                nodes=inside_points[i]
                intersection=list_of_intersections[i]
                for k in range(len(temp_triangle)-1):
                    if points[temp_triangle[k]]!=nodes[0]:
                        nodes.append(points[temp_triangle[k]])
                intersection2=[]
                for k in range(len(intersection)):
                    if abs((nodes[0].y-intersection[k].y)/(nodes[0].x-intersection[k].x)-(nodes[0].y-nodes[1].y)/(nodes[0].x-nodes[1].x))<0.00001:
                        intersection2.append(intersection[k])
                    elif abs((nodes[0].y-intersection[k].y)/(nodes[0].x-intersection[k].x)-(nodes[0].y-nodes[2].y)/(nodes[0].x-nodes[2].x))<0.0001:
                        intersection2.append(intersection[k])
                    if len(intersection2)==2:
                        if intersection2[0].x==intersection2[1].x and intersection2[0].y==intersection2[1].y:
                            intersection2.pop()
                if len(intersection)==4:
                    print(len(intersection2))
                    for k in range(4):
                        if intersection[k]!=intersection2[0] and intersection[k]!=intersection2[1]:
                            intersection2.append(intersection[k])
                    distance=length
                    for k in rectangle_vertices:
                        if distance>Length(k-intersection2[2]):
                            temp4=k
                            distance=Length(k-intersection2[2])
                    area_inside_rectangle[i]=area([intersection2[0],intersection2[1],nodes[0]])+area([temp4,intersection2[0],intersection2[1]])-area([temp4,intersection2[2],intersection2[3]])
                elif len(intersection)==3:
                    area_inside_rectangle[i]=area([intersection2[0],intersection2[1],nodes[0]])
        elif count2==1:
            temp4=[]
            if len(list_of_intersections[i])==2:

                for k in list_of_intersections[i]:
                    temp4.append(k)
                temp4.append(inside_rec_point)
                area_inside_rectangle[i]=area(temp4)
                temp2=inside_points[i]
                temp4[2]=temp2[0]
                area_inside_rectangle[i]=area_inside_rectangle[i]+area(temp4)
            elif len(list_of_intersections[i])==3:

                for k in list_of_intersections[i]:
                    temp4.append(k)
                area_inside_rectangle[i]=area(temp4)
                for k in range(len(temp4)):
                    if abs(temp4[k].x-inside_rec_point.x)<0.0001 and abs(temp4[k].y-inside_rec_point.y)<0.0001:
                        temp2=inside_points[i]
                        temp4[k]=temp2[0]
                area_inside_rectangle[i]=area_inside_rectangle[i]+area(temp4)
                if abs(temp4[0].x-temp4[1].x)<0.00001 and abs(temp4[0].y-temp4[1].y)<0.00001:
                    temp4[0]=inside_rec_point
                elif abs(temp4[0].x-temp4[2].x)<0.00001 and abs(temp4[0].y-temp4[2].y)<0.00001:
                    temp4[0]=inside_rec_point
                elif abs(temp4[2].x-temp4[1].x)<0.00001 and abs(temp4[2].y-temp4[1].y)<0.00001:
                    temp4[2]=inside_rec_point
                area_inside_rectangle[i]=area(temp4)
            elif len(list_of_intersections[i])==4:
                for k in list_of_intersections[i]:
                    temp4.append(k)
                temp5=[]
                temp5.append(temp4[0])
                if temp4[1].x!=temp5[0].x or temp4[1].y!=temp5[0].y:
                    temp5.append(temp4[1])
                elif temp4[2].x!=temp5[0].x or temp4[2].y!=temp5[0].y:
                    temp5.append(temp4[2])
                else:
                    temp5.append(temp4[3])
                temp2=inside_points[i]
                temp5.append(temp2[0])
                area_inside_rectangle[i]=area(temp5)
                count3=1
                for k in temp5:
                    if (k.x!=temp4[0].x or k.y!=temp4[0].y) and (k.x!=temp4[1].x or k.y!=temp4[1].y) and (k.x!=temp4[2].x or k.y!=temp4[2].y) and (k.x!=temp4[3].x or k.y!=temp4[3].y):
                        count3=0
                if count3==0:

                    for j in rectangle_vertices:
                        for p in temp4:
                            if j.x==p.x and j.y==p.y:
                                temp7=p

                    temp5=[]
                    for j in temp4:
                        if j.x!=temp7.x or j.y!=temp7.y:
                            temp5.append(j)
                    temp2=inside_points[i]
                    temp5.append(temp2[0])
                    area_inside_rectangle[i]=area(temp5)+area([temp5[0],temp5[1],temp7])



            else:
                for k in list_of_intersections[i]:
                    temp4.append(k)
                temp5=[]
                temp5.append(temp4[0])
                if temp4[1].x!=temp5[0].x or temp4[1].y!=temp5[0].y:
                    temp5.append(temp4[1])
                elif temp4[2].x!=temp5[0].x or temp4[2].y!=temp5[0].y:
                    temp5.append(temp4[2])
                elif temp4[3].x!=temp5[0].x or temp4[3].y!=temp5[0].y:
                    temp5.append(temp4[3])
                else:
                    temp5.append(temp4[4])
                temp2=inside_points[i]
                temp5.append(temp2[0])
                area_inside_rectangle[i]=area(temp5)
    print(area_inside_rectangle)
    total=0
    for i in area_inside_rectangle:
        total=total+i
    print (total)
#mesh parameters
l=3 #length of triangle
h=13 #number of rows
n=7 #number of columns
#circle parameters
radius=2 #radius of circle
circle_center=find_center_of_circle(n,h,l)
#rectangle parameters
length=11
width=6
normal=vector(11,100)
bottom_point=vector(10,21)


points=create_points(h,n,l)
test=unstructured_mesh(points,l,h,n)
triangler=test.triangles()
volume_fraction=find_volume_fraction(points,triangler,n,h,l,radius,circle_center)
normal_x,normal_y=find_normal(points,triangler,volume_fraction,circle_center)
rectangle_vertices=find_height_function_vertices(length,width,normal,bottom_point)
create_text(n,h,points,triangler,volume_fraction,normal_x,normal_y,rectangle_vertices)
find_height_function(rectangle_vertices,points,triangler)




