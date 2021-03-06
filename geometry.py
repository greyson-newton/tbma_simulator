# 3X3 MATRIX INITIALIZED WITH ALL 0's
#https://developer.rhino3d.com/guides/rhinopython/python-rhinoscriptsyntax-introduction/
from logging import makeLogRecord
from math import *
from collections import namedtuple
from types import *
from matplotlib import interactive
import numpy as np
from matplotlib.cbook import index_of
from scipy.stats.stats import obrientransform  
# we can test for lambda type, e.g.:
# class intersect_line_w_plane():
    # Need a method to check 
    # Needs methods to return hit coordinates, slope if intersect true
    # See how it was done in chamber->getResiduals() part from the old program
            # interceptTrack = intersectAndHit(self.designEndpoints, muonTrack)

            # #did it hit the chamber
            # track =False
            # minVal, maxVal = min(self.designEndpoints[1]), max(self.designEndpoints[1])
            # if interceptTrack[1] < maxVal and interceptTrack[1] > minVal:
            #     track = True

            # #find local dy/dx
            # trackSlope = returnLocalDxDy(self.designAngle, muonTrack)
            # transformedInterceptTrack = transformCord(self.designX, self.designY, self.designAngle, interceptTrack)

    # Needs to return below and more in Vec3 
        # self.hit = Vec.3()
        # self.hitXOverY = []

        # self.track = [[],[]]
        # self.trackXOverY = []   

# Call isinstance(object, class_or_tuple) with class_or_tuple 
# as list to return True if object is an instance or subclass of list and False if otherwise.
class Point3(object):
    '''Creates a point on a coordinate plane with values x,y,z'''

    def __init__(self, p=None):
        self.x,self.y,self.z=0.,0.,0.
        if p==None:
            self.x,self.y,self.z=0.,0.,0.
        elif isinstance(p,list):
            if type(p[0])!=Point3:
                self.x, self.y,self.z = float(p[0]),float(p[1]),float(p[2])
            else:
                print("wtf")
                # print(type(p))
        elif isinstance(p,Point3):
            self.x, self.y,self.z = p.x,p.y,p.z
        else:
            print("not list")

    def add(self,p): #returns a point representing sum of two points  
        if isinstance(p,list):
            self.x+=p[0]
            self.y+=p[1]
            self.z+=p[2]
        elif type(p) == Point3:
            return Point3([self.x+p.x,self.y+p.y,self.z+p.z])
        else:
            print("invalid")
            return None
    def sub(self,p): #returns a point representing sum of two points  
        if isinstance(p,list):
            return Point3(self.x-p[0],self.y-p[1],self.z-p[2])
        elif type(p) == Point3:
            return Point3(self.x-p.x,self.y-p.y,self.z-p.z)
        else:
            print("invalid")
            return None
    def scale(self,fact):
        if type(fact)==Point3:
            self.x,self.y,self.z=self.x*fact.x,self.y*fact.y,self.z*fact.z
        else:
            self.x,self.y,self.z=self.x*fact,self.y*fact,self.z*fact
    def to_string(self):
        return "Point(%s,%s)"%(self.x,self.y,self.z) 
    def distance(self, p):
        dx,dy,dz = (self.x - p.x),(self.y - p.y),(self.z - p.z)  
        return sqrt(dx**2 + dy**2+dz**2)
    def to_vector(self,p=None):
        #from self.pt to the arbitra.head.y Point3 p
        if p==None:
            return Vec3(self.pt)
        else:
            return Vec3(p).sub(Vec3(self.pt))
    def to_list(self):
        return [self.x, self.y,self.z]
    def out(self):
        return "(%s,%s,%s)"%(self.x,self.y,self.z) 
    def set(self,coord):
        self.x,self.y,self.z=coord[0],coord[1],coord[2]
zero_pt = Point3([0.,0.,0.])
def is_zero_pt(pt):
    if pt.x==zero_pt.x:
        if pt.y==zero_pt.y:
            if pt.z==zero_pt.z:
                return True
    else:
        return False
def return_angles(l):
    x,y,z = l[0],l[1],l[2]
    if x!=0:
        theta = atan(z/x)
        mag = hypot(z,x)
        if mag!=0:
            phi = atan(y/mag)
            mag = hypot(y,mag)
            return [theta,phi]
        else:
            return [theta,0.0]
    else:
        return [0.,0.]        
def sub(p1,p2):
    return Point3([p2.x-p1.x,p2.y-p1.y,p2.z-p1.z])
class line:
    def __init__(self,p):
        #given one point, make it from origin to point
        self.pts=[Point3([0.,0.,0.]),Point3([0.,0.,0.])]
        self.magnitudes=[0.,0.,0.] 
        self.angles= [0.,0.,0.]
        if type(p)==list:
            # print('line given list')
            if type(p[0])==Point3 and len(p)==2:
                # print('     of 2 Points')
                self.magnitudes=[p[1].x-p[0].x,p[1].y-p[0].y,p[1].z-p[0].z]     
                self.pts=[p[0],p[1]]
                self.angles= return_angles(self.magnitudes)
            elif type(p[0])==float and len(p)==3:
                # print('     of 3 floats')
                p = Point3(p)
                self.magnitudes=[p.x,p.y,p.z]     
                self.pts=[Point3([0.,0.,0.]),p]
                self.angles= return_angles(self.magnitudes)
            else:
                print(type(p[0]))
            
        elif type(p)==Point3:
            # print('line given one point - a 000 tail')
            # print(p.x,p.y,p.z)
            self.pts=[Point3([0.,0.,0.]),p]
            self.magnitudes=[p.x,p.y,p.z] 
            self.angles= return_angles(self.magnitudes)
        else:
            self.pts=[Point3([0.,0.,0.]),Point3([0.,0.,0.])]
            self.magnitudes=[0.,0.,0.] 
            self.angles= [0.,0.,0.]
        # if sqrt(self.magnitudes[0]**2+self.magnitudes[1]**2+self.magnitudes[2]**2)!=0:
        #     self.normalize()
    def normalize(self):
        # print("NORMALIZING")
        fact=(1/sqrt(self.magnitudes[0]**2+self.magnitudes[1]**2+self.magnitudes[2]**2))
        # print(fact)
        self.magnitudes = [mag*fact for mag in self.magnitudes]
        # print("DONE")
    def set(self,p):
        self.pts[0],self.pts[1]=p[0],p[1]
        self.normalize()
        self.angles=return_angles(self.magnitudes)
    def scale(self,fact):
        self.pts[0].scale(fact)
        self.pts[1].scale(fact)
        # return line(self.pts)
    def sub(self,l):
        s = [self.pts[0].x-l.pts[0].x,self.pts[0].y-l.pts[0].y,self.pts[0].z-l.pts[0].z]
        p = [self.pts[1].x-l.pts[1].x,self.pts[1].y-l.pts[1].y,self.pts[1].z-l.pts[1].z]
        return line([s,p])
    def radd(self,l):
        if type(l)==list:
            self.pts[0].x+=l[0]
            self.pts[0].y+=l[1]
            self.pts[0].z+=l[2]
            self.pts[1].x+=l[0]
            self.pts[1].y+=l[1]
            self.pts[1].z+=l[2]

    #make this global, not a part of a class
    def add(self,l):
        s = [self.pts[0].x+l.pts[0].x,self.pts[0].y+l.pts[0].y,self.pts[0].z+l.pts[0].z]
        p = [self.pts[1].x+l.pts[1].x,self.pts[1].y+l.pts[1].y,self.pts[1].z+l.pts[1].z]
        return line([s,p])
    
    def out(self):
        p1o,p2o=self.pts[0].out(),self.pts[1].out()
        return "\n  Line\n      magnitude (%s,%s,%s)"%(self.magnitudes[0],self.magnitudes[1],self.magnitudes[2])+"\n        Endpts[ "+p1o+' -> '+p2o+' ]'
def cross(b,a):
    # print("LINE CROSS")
    x,y,z = b.magnitudes[0],b.magnitudes[1],b.magnitudes[2]
    ax,ay,az = a.magnitudes[0],a.magnitudes[1],a.magnitudes[2]
    # print(x,y,z,ax,ay,az)
    # print(y*az-z*ay,x*az-z*ax,x*ay-y*ax)
    mag = Point3([y*az-z*ay , -(x*az-z*ax), x*ay-y*ax])
    # print(mag.x,mag.y,mag.z)
    cross = Vec3(mag)
    # print(len(cross.lines))
    # print(cross.head_magnitude)
    return mag       
class Vec2:
    def __init__(self,x,y):
        self.x=x,self.y=y               
class Vec3: 
    #  3D VECTOR
    def __init__(self,p1):
        #A list of points - like a linked list.
        #Other words a list of lines, with info on directional magnitude
        self.norm=Point3([0.,0.,0.])
        self.pts = [Point3([0.,0.,0.]),Point3([0.,0.,0.])]
        self.mag = Point3(zero_pt)
        if type(p1)==Point3:
            self.pts.append(p1)
        #put in tuple - connect them all
        self.lines = [[],[]]
        if type(p1)==list:
            if len(p1)==2 and type(p1[0])==Point3:
                l =line([p1[0],p1[1]])
                self.pts=[p1[0],p1[1]]
                self.mag=sub(p1[0],p1[1])
                self.lines[0]=l
            if type(p1[0])==float and len(p1)==3:
                p1=Point3(p1)
                l=line([Point3([0.,0.,0.]),p1])
                self.lines[0]=[l]
            if type(p1[0]) == Point3:
                if len(p1)==2:
                    l = line(p1)  
                    self.lines[0]=[l]
                    self.pts=[p1[0],p1[1]]
                else:
                    # print('handling list of pts greater than 2')
                    count=0
                    self.pts[0]=p1[0]
                    lastpt=p1[0]
                    for pt in p1:
                        if count==0:
                            lastpt=pt
                            count+=1
                        if count==1:
                            self.pts[1]=pt
                            l=line([lastpt,pt])
                            self.lines[0]=[l]
                            count+=1
                            lastpt=pt
                        if count==2:
                            self.pts.append(pt)
                            l=line([lastpt,pt])
                            self.lines[1]=[l]
                            count+=1
                            lastpt=pt
                        else:
                            self.pts.append(pt)
                            l=line([lastpt,pt])
                            self.lines+=[l]
                            count+=1
                            lastpt=pt
        else:
            if type(p1)==Point3:
                # print('else')
                l=line(p1)
                # print(l.out())
                self.lines[0]=l
                                       #last point in last line, first point in first line

        self.head=Point3()
        self.tail=Point3()
        self.head_magnitude = [self.head.x-self.tail.x,self.head.y-self.tail.y,self.head.z-self.tail.z]
        self.dir_vector = [0.,0.,0.]
        self.check_vec()
        
        # self.update_vector()
    def ret_mag(self):
        return Point3([self.pts[-1].x-self.pts[0].x,self.pts[-1].y-self.pts[0].y,self.pts[-1].z-self.pts[0].z])
    def update_pts(self,translation):
        # print("UPDATE PTS")
        if type(translation)==list:
            translation=Point3(translation)
        count=0
        # print("length ",len(self.pts))
        size =len(self.pts)
        if size>4:
            self.pts=[self.pts[size-4],self.pts[size-3],self.pts[size-2],self.pts[size-1]]
        for pt in self.pts:
            # print(pt.out())
            if count==0:
                continue
            pt.x+=float(translation.x)
            pt.y+=float(translation.y)
            pt.z+=float(translation.z)
            count+=1
        self.update_lines()
        return self.pts
    def update_lines(self):
        # print("length ",len(self.lines))

        self.lines[0]=line([self.pts[0],self.pts[1]])
        self.lines[1]=line([self.pts[1],self.pts[2]])
        self.lines[2]=line([self.pts[2],self.pts[3]])
        self.lines[3]=line([self.pts[3],self.pts[0]])
        
    def __add__(self,p):   #adds a point or coordinate list to vector 
        if isinstance(p,list):
            if type(p[0])==float:
                p = Point3(p)
        if type(p)==Point3:
            l = line(self.head,p)
            if len(self.lines)==2:
                self.lines[1]=[l]
            elif len(self.lines)>2:
                self.lines+=l  
        self.update_head()
    def add(self,a):
        if type(a) == list:
            return Vec3(a.head.x+self.head.x, a.head.y+self.head.y, a.head.z+self.head.z)
        elif type(a) == Vec3:
            return Vec3(a.head.x+self.head.x, a.head.y+self.head.y, a.head.z+self.head.z)
        else:
            print("invalid")

    def sub(self,a):
        if type(a) == list:
            return Vec3([a.head.x-self.head.x, a.head.y-self.y, a.head.z-self.z])
        elif type(a) == Vec3:
            pts=[]
            if len(self.pts)==len(a.pts):
                for p1,p2 in zip(self.pts,a.pts):
                    pts.append(Point3([p1.x-p2.x,p1.y-p2.y,p1.z-p2.z]))
                return Vec3(pts)
        else:
            print("invalid")



    def scale_by_matrix(self, mat3):
        # MULTIPLIES A Vec3 OBJECT WITH Mat3 OBJECT AND RETURNS A NEW Vec3 
        x = self.head.x * mat3.matrix[0][0] + self.head.y * mat3.matrix[0][1] + self.head.z * mat3.matrix[0][2]
        y = self.head.x * mat3.matrix[1][0] + self.head.y * mat3.matrix[1][1] + self.head.z * mat3.matrix[1][2]
        z = self.head.x * mat3.matrix[2][0] + self.head.y * mat3.matrix[2][1] + self.head.z * mat3.matrix[2][2]
        return Vec3(x, y, z)
    def scale_by_factor(self, fact):
        # MULTIPLIES A self OBJECT WITH Mat3 OBJECT AND RETURNS A NEW self 
        # print("SCALING")
        li=[]
        for l in self.lines:
            pts = [Point3([l.pts[0].x*fact,l.pts[0].y*fact,l.pts[0].z*fact]),
                    Point3([l.pts[1].x*fact,l.pts[1].y*fact,l.pts[1].z*fact])]
            li.append(line(pts))
        self.lines=[] 
        for l in li:
            self.lines.append(l)
        if type(self.head) ==Point3 and type(self.tail) == Point3:
            self.mag=[self.pts[-1].x-self.pts[0].x,self.pts[-1].y-self.pts[0].y,self.pts[-1].z-self.pts[0].z] 
        self.check_vec()
        # self.out_all()
    def ret_magnitude(self):
        return hypot(self.head.x,self.head.y,self.head.z)
    def out_head(self):
        return '\nHead of vector: '+self.pts[-1].out()+'\n'
    def out_all(self,square=None):
        if square==True:
            print('Lines that make up this Square ')
            for l in self.lines:
                if type(l)==line:
                    print(l.out())
        else:
            print(self.out_head())
            print('   Lines that make up this vector ')
            for l in self.lines:
                if type(l)==line:
                    print(l.out())
    def normalize(self):
        # print("NORMALIZING")
        mag=self.ret_mag()
        fact=(1/sqrt(mag.x**2+mag.y**2+mag.z**2))
        # print(fact)
        self.norm = Point3([mag.x*fact,mag.y*fact,mag.z*fact])
        # print("DONE")
    def check_vec(self):
        count=0
        indexes=[]
        ind=[]
        l = []
        # print(type(l))

        for count in range(len(self.lines)):
            if type(self.lines[count])==list:
                if len(self.lines[count]) !=0 and type(self.lines[count][0])==None:
                    print("none")
                    indexes.append(count)
                    count+=1
                if len(self.lines[count])>0 and self.lines[count][0]==line:
                    ind.append(count)
                    l.append(self.lines[count][0])
                    count+=1
            if type(self.lines[count])==None:
                print("none")
                indexes.append(count)
                count+=1
            else:
                if type(self.lines[count])==line:
                    ind.append(count)
                    # print(type(l))
                    l.append(self.lines[count])
                    count+=1
        # print(indexes)
        # print(ind)
        self.lines = []

        for every in l:     
            if is_zero_pt(every.pts[0]) and is_zero_pt(every.pts[1]):
                continue
            else:
                
                self.lines.append(every)

    def ret_tail_head(self):
        if len(self.lines)==1:
            return [self.lines[0].pts[0],self.lines[0].pts[1]]
        # print(len(self.lines))
        return [self.lines[0].pts[0],self.lines[-1].pts[1]]
    # def update_vector(self):
    #     x,y,z=0.,0.,0.
    #     for l in self.lines:
    #         x+=l.magnitudes[0]
    #         y+=l.magnitudes[1]
    #         z+=l.magnitudes[2]
    #     self.head_magnitude = [x,y,z]

def make_vector(p1,p2=None):
    if p2==None:
        return Vec3(p1)
    else:
        v0,v1 = Vec3(p1),Vec3(p2)
        return v1.sub(v0)
def dot(a,b):
    # print("fuck this ",type(a),type(b))
    dot=0.
    if type(a)==Vec3 and type(b)==Vec3:
        dot=a.ret_mag().x*b.ret_mag().x+a.ret_mag().y*b.ret_mag().y+a.ret_mag().z*b.ret_mag().z
    if type(a)==Point3 and type(b)==Point3:
        # print("fuck")
        dot = (a.x*b.x)+(a.y*b.y)+(a.z*b.z)
        # print("dot " ,dot," and type ",type(dot))
    if type(a)==Point3 and type(b)==Vec3:
        dot=(a.x*b.ret_mag().x) + (a.y*b.ret_mag().y) + (a.z*b.ret_mag().z)
        # print("dot p \w v: ", str(dot))
    return dot
    # if len(a.pts)==2:
    #     return a.pts.x*b.pts.x+a.pts.y*b.y+a.pts.z*b.pts.z
    #     print("line dot")
    # elif len(a.pts)>2:
    #     dot=a.pts[-1].x*b.pts[-1].x+a.pts[-1].y*b.pts[-1].y+a.pts[-1].z*b.pts[-1].z
    #     # print("dot ",dot," type ",type(dot))
    #     return dot
    # else:
    #     print("cant dot")
def cross(a,b):
    print("VEC3 CROSS")
    return Vec3(Point3([a.y*b.z-a.z*b.y , -(a.x*b.z-a.z*b.x), a.x*b.y-a.y*b.x]))

class Mat3:
    # 3X3 MATRIX INITIALIZED WITH ALL 0's
    def __init__(self,data=None):
        if data==None:
            self.matrix = [[0 for i in range(3)],
                        [0 for i in range(3)],
                        [0 for i in range(3)]]
        elif type(data)==list and type(data[0])==list:
            if data[0][0]==Vec3:
                self.matrix = [data[0],
                            data[1],
                            data[2]]

def normal_vec(p0,p1,p2):
    # print("NORMAL VECTOR")
    # https://stackoverflow.com/questions/63050302/ploting-the-normal-vector-to-a-plane
    if type(p0)==Point3 and type(p1)==Point3 and type(p2)==Point3:
        ux, uy, uz = u = [p1.x-p0.x, p1.y-p0.y, p1.z-p0.z] #first vector
        vx, vy, vz = v = [p2.x-p0.x, p2.y-p0.y, p2.z-p0.z] #sec vector
        u_cross_v =Point3([uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx])#cross product
        d=dot(p1,u_cross_v)
        # print('plane equation:\n{:1.4f}x + {:1.4f}y + {:1.4f}z + {:1.4f} = 0'.format(u_cross_v.x, u_cross_v.y, u_cross_v.z, d))
              # print("NORMALIZING")
        return u_cross_v

def scale_by_matrix(line, mat3):
    # MULTIPLIES A Vec3 OBJECT WITH Mat3 OBJECT AND RETURNS A NEW Vec3 
    ref = line
    p1,p2=line.pts[0],line.pts[1]
    # print("scaling : " + line.out())
    p1.set([p1.x * mat3.matrix[0][0] + p1.y * mat3.matrix[0][1] + p1.z * mat3.matrix[0][2],
            p1.x * mat3.matrix[1][0] + p1.y * mat3.matrix[1][1] + p1.z * mat3.matrix[1][2],
            p1.x * mat3.matrix[2][0] + p1.y * mat3.matrix[2][1] + p1.z * mat3.matrix[2][2]])

    p1.set([p2.x * mat3.matrix[0][0] + p2.y * mat3.matrix[0][1] + p2.z * mat3.matrix[0][2],
            p2.x * mat3.matrix[1][0] + p2.y * mat3.matrix[1][1] + p2.z * mat3.matrix[1][2],
            p2.x * mat3.matrix[2][0] + p2.y * mat3.matrix[2][1] + p2.z * mat3.matrix[2][2]])
    # print(" ->"+ line.out())
    # print("difference - "+ref.sub(line).out())
class Transform:
    # IT TRANSFORMS THE X AND Y FROM NORMALIZED SPACE TO SCREEN SPACE WITH PROJECTION APPLIED
    def worldSpaceTransform(vec3, w, h):
        if vec3.magnitudes[0] == 0:
            vec3.magnitudes[0] = 0.001
        zInverse = 1/ vec3.magnitudes[0] 
        xTransformed = ((vec3.magnitudes[2] * zInverse) + 1) * (w/2)
        yTransformed = ((-vec3.magnitudes[1] * zInverse) + 1) * (h/2)
        xTransformed = str(xTransformed)[:6]
        yTransformed = str(yTransformed)[:6]
        return [float(xTransformed), float(yTransformed)]

# Implement y and z axis rotation matrices
class Rotation: 
    def __init__(self):
        self.current_rotation=[0,0,0]
def rotateX(theta):
    # ROTATION MATRIX IN X AXIS
    sinTheta = sin(theta)
    cosTheta = cos(theta)
    m = Mat3()
    m.matrix = [[1, 0,         0],
                [0, cosTheta,  sinTheta],
                [0, -sinTheta, cosTheta]]
    return m
def rotateY(theta):
    # ROTATION MATRIX IN X AXIS
    sinTheta = sin(theta)
    cosTheta = cos(theta)
    m = Mat3()
    m.matrix = [[cosTheta, 0,  sinTheta],
                [0, 1,  0],
                [-sinTheta, 0, cosTheta]]
    return m
def rotateZ(theta):
    # ROTATION MATRIX IN X AXIS
    sinTheta = sin(theta)
    cosTheta = cos(theta)
    m = Mat3()
    m.matrix = [[cosTheta,  sinTheta,  0],
                [-sinTheta, cosTheta,  0],
                [0, 0, 1]]
    return m

#Make to be initialized empty,list,and another pt

def normalize(vec):
    m=vec.ret_mag()
    fac=sqrt(m.z**2+m.y**2+m.x**2)
    if fac != 0:
        return Point3([m.x/fac,m.y/fac,m.z/fac])
class Square:
    def __init__(self,pts,origin):
        self.rotator = Rotation()
        self.transform = Transform()
        
        self.origin=Point3(zero_pt)
        self.origin.add(origin)
        self.endpoints=pts
        self.square_vec=Vec3(pts)
        size=len(self.square_vec.pts)
        # print("NUM OF PTS IN SQUARE VEC ", size)
        if len(self.square_vec.pts)>5:
            pts=self.square_vec.pts
            self.square_vec.pts=[pts[size-1],pts[size-2],pts[size-3],pts[size-4],pts[size-5]]
            # for p in self.square_vec.pts:
                # print("AHHH ",p.out())
        self.current_rotation=[0.,0.,0.]
        # self.normal_vector = normal_vec(self.square_vec)
        # print("SQUARE NORMAL :")
        # print(self.normal_vector.lines)
        # print("NUM OF SQUARE PTS ON INIT ",len(pts))

    def out(self):
        # print("SQUARE")
        # print("\nnormal vector: "+self.normal_vector.lines[0].out())
        return self.square_vec.out_head(square=True)
    def plot_out(self):
        # if rot==True:
        #     x,y=[],[]
        #     for l in self.square_vec.lines:
        #         x.append(Transform.worldSpaceTransform(l,5,5)[0])
        #         y.append(Transform.worldSpaceTransform(l,5,5)[1])
        #         return [x,y]
        # else:
        # x,y,z=[],[],[]
        # for pt in self.square_vec.pts:
        #     x.append(pt.x)
        #     y.append(pt.y)
        #     z.append(pt.z)
        # return zip(x,y,z)

        
        
        
        return [[self.square_vec.pts[0].x,self.square_vec.pts[1].x,
                self.square_vec.pts[2].x,self.square_vec.pts[3].x,
                self.square_vec.pts[0].x],
            
                [self.square_vec.pts[0].y,self.square_vec.pts[1].y,
                self.square_vec.pts[2].y,self.square_vec.pts[3].y,
                self.square_vec.pts[0].y],

                [self.square_vec.pts[0].z,self.square_vec.pts[1].z,
                self.square_vec.pts[2].z,self.square_vec.pts[3].z,
                self.square_vec.pts[0].z]]
    
    def rotate(self,rotations):
        # ROTATES A Vec3 (a) BY GIVEN THETA AND AXIS
        
        current_rotation=[0.,0.,0.]
        if type(rotations)==Point3:
            theta,eta,phi=rotations.x,rotations.y,rotations.z
        else:
            theta,eta,phi=rotations[0],rotations[1],rotations[2]

        # mx,my,mz = rotateX(theta)
        if theta != 0:
            current_rotation[0]=theta
            for l in self.square_vec.lines:
                scale_by_matrix(l, rotateX(theta))
                # l.scale(Point3([cos(theta),.,1.]))
        if eta != 0:
            current_rotation[1]=eta
            for l in self.square_vec.lines:
                scale_by_matrix(l, rotateY(eta))
        if phi !=0 :
            current_rotation[2]=phi
            for l in self.square_vec.lines:
                scale_by_matrix(l, rotateZ(phi))
        self.normal_vector = normal_vec(self.square_vec.pts[0],self.square_vec.pts[1],self.square_vec.pts[2])
        # for l in self.square_vec.lines:
        #     l.scale(self.normal_vector)
        self.endpoints=[self.square_vec.lines[0].pts[0],self.square_vec.lines[1].pts[0],
                        self.square_vec.lines[2].pts[0], self.square_vec.lines[3].pts[0]]
        return self.current_rotation
    # def update(self):
    # def update_endpoint(self,index):
    #     if index=1:
    #     if index=2:
    #     if index=3:
    #     if index=4:
    def has_rotation(self):
        for rot in self.current_rotation:
            if rot !=0:
                return False
            else:
                return True
    def translate(self,translations,des):
        # flip_rot=[]
        # if self.has_rotation():
        #     for rot in self.current_rotation:
        #         flip_rot.append(-rot)
        #     self.rotate(flip_rot)

        # l_c=0
        # for l in self.square_vec.lines:
        #     for pt in l.pts:
        #         print(pt.out())
        self.origin.add(translations)
        self.square_vec.pts=[pt.add(translations)for pt in self.square_vec.pts]
        # if des==True:
        #     for en in self.square_vec.pts:
        #         print("design pts ",en.out())
        # else:
        #     for en in self.square_vec.pts:
        #         print("actual pts ",en.out())
        self.endpoints=self.square_vec.pts
        # print("did translation work?")
        # for en in self.endpoints:
        #     print(en.out())
            #     # l.pts[1].add(translations)
            # else:
            #     for pt in l.pts:
            #         pt.add(translations)
        # self.rotate(self.current_rotation)
        # self.square_vec.lines[2].pts[0].add(translations)
        # self.square_vec.lines[1].pts[1].add(translations)
        # self.square_vec.lines[3].pts[0].add(translations)

        # self.endpoints=[self.square_vec.lines[0].pts[0],self.square_vec.lines[1].pts[0],
        #                 self.square_vec.lines[2].pts[0], self.square_vec.lines[3].pts[0]]
        # self.rotate(self.current_rotation)
    def intersect_with(self,muon, cham_origin,epsilon=1e-6):
        # print("INTERSECT WITH")
        p0,p1,p2 = cham_origin,self.endpoints[0],self.endpoints[1]
        mp0,mp1=muon.track.pts[0],muon.track.pts[-1]
        # print("p0,p1,p2: ",p0.out(),p1.out(),p2.out())
        # print("mpo,mp1: ", mp0.out(), mp1.out())

        n=normal_vec(p0,p1,p2)
        # print("normal plane: ", n.out())

        a=make_vector(mp0,p0)
        b=make_vector(mp0,mp1)
        # print("p0-mp0: ", a.out_all())
        # print("mp1-mp0: ", b.out_all())

        top = dot(n,a)
        bottom = dot(n,b)
        d=top/bottom
        # print("d factor: ", d)
        # b.scale_by_factor(d)
        b.pts[-1]=Point3([ b.pts[-1].x*d,  b.pts[-1].y*d,  b.pts[-1].z*d ])
        # print(b.out_head())

        
        x,y,z=[],[],[]
        for endpt in self.endpoints:
            z.append(endpt.z)
            y.append(endpt.y)
            x.append(endpt.x)
        boundz,boundy,boundx=[z[0],z[1]],[y[0],y[1]],[x[0],x[1]]
        for xp in x:
            if xp<boundx[0]:
                boundx[0]=xp
            if xp>boundx[1]:
                boundx[1]=xp
        for zp in z:
            if zp<boundz[0]:
                boundz[0]=zp
            if zp>boundz[1]:
                boundz[1]=zp
        for yp in y:
            if yp<boundy[0]:
                boundy[0]=yp
            if yp>boundy[1]:
                boundy[1]=yp
        hit=b.pts[-1]
        print("        Projected point of Muon-Chamber intersection: ", hit.out())
        print("        Checking Bounds\n        BOUNDS: [zi,zf], [yi,yf]: [", str(boundz[0]), "," , str(boundz[1]), "] [",str(boundy[0]), ",",str(boundy[1]),"]")
        if hit.z > boundz[0] and hit.y > boundy[0] and hit.z < boundz[1] and hit.y < boundy[1]:
            print("          intersection within chamber bounds!! : ")
            print("          hit at: ", hit.out())
            return hit
        elif hit.z <  boundz[0] and hit.z > boundz[1]:
            print("          outside z bounds ")
            return None
        elif hit.y < boundy[0] and hit.y > boundy[1]:
            print("          outside y bounds ")
            return None
        
        # norm = normal_vec(self.endpoints)

        # for zp,yp in zip(boundz,boundy):
        #     print(type(zp),type(yp))
        # for p in w.pts:
        #     print(type(p))


# p4 = Point3([-4.,0.,4.])
# p3 = Point3([9.,-3.,-1.])
# p2 = Point3([5.,3.,4.])
# p1 = Point3([1.,1.,1.])
# v=Vec3([p1,p2,p3,p4])
# print(v.out_all())
# f=5
# v.scale_by_factor(f)
# print(v.out_all)


# old intersection
        # """
        # p0, p1: Define the line.
        # p_co, p_no: define the plane:
        #     p_co Is a point on the plane (plane coordinate).
        #     p_no Is a normal vector defining the plane direction;
        #         (does not need to be normalized).

        # Return a Vector or None (when the intersection can't be found).
        # """
        # # print(self.normal_vector.out_all())
        # # print("muon",muon.track.out_all())
        # self.normal_vector.check_vec()
        # # print(type(muon.track),type(self.normal_vector))
        # d = dot(muon.track,self.normal_vector)
        
        # if abs(d) > epsilon:
        #     # The factor of the point between p0 -> p1 (0 - 1)
        #     # if 'fac' is between (0 - 1) the point intersects with the segment.
        #     # Otherwise:
        #     #  < 0.0: behind p0.
        #     #  > 1.0: infront of p1.
        #     w = make_vector(origin,muon.p_f)
        #     w.check_vec()
        #     # print(w.out_all())
        #     if d==0:
        #         d=.00001
        #     fac = -1*(dot(self.normal_vector,w) / d)
        #     w.scale_by_factor(fac)
        #     # print(w.out_all)
    #     if len(w.lines)==1:
    #         hit=w.lines[0].pts[1]
    #         print("hit candidate: "+hit.out())
    #         if hit.y > boundy[1] or hit.y < boundy[0] or hit.z > boundz[1] or hit.z < boundz[0]:
    #             print("outside chamber")
    #             return None
    #         else:
    #             print("intersection found at: ",hit.out())
    #             return hit
    #     else:
    #         print("no go")
    # else:
    #     # The segment is parallel to plane.
    #     print("parralell")
    #     return None