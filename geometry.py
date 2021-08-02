# 3X3 MATRIX INITIALIZED WITH ALL 0's
#https://developer.rhino3d.com/guides/rhinopython/python-rhinoscriptsyntax-introduction/
from math import *
from collections import namedtuple
from types import *  
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
        elif isinstance(p,Point3):
            self.x, self.y,self.z = p.x,p.y,p.z
        else:
            print("not list")

    def add(self,p): #returns a point representing sum of two points  
        if isinstance(p,list):
            return Point3(self.x+p[0],self.y+p[1],self.z+p[2])
        elif type(p) == Point3:
            return Point3(self.x+p.x,self.y+p.y,self.z+p.z)
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
        
class line:
    def __init__(self,p):
        #given one point, make it from origin to point
        self.pts=[Point3([0.,0.,0.]),Point3([0.,0.,0.])]
        self.magnitudes=[0.,0.,0.] 
        self.angles= [0.,0.,0.]
        if type(p)==list:
            print('line given list')
            if type(p[0])==Point3 and len(p)==2:
                print('     of 2 Points')
                self.magnitudes=[p[1].x-p[0].x,p[1].y-p[0].y,p[1].z-p[0].z]     
                self.pts=[p[0],p[1]]
                self.angles= return_angles(self.magnitudes)
            elif type(p[0])==float and len(p)==3:
                print('     of 3 floats')
                p = Point3(p)
                self.magnitudes=[p.x,p.y,p.z]     
                self.pts=[Point3([0.,0.,0.]),p]
                self.angles= return_angles(self.magnitudes)
            else:
                print(type(p[0]))
            
        elif type(p)==Point3:
            print('line given one point - a 000 tail')
            print(p.x,p.y,p.z)
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
        print("NORMALIZING")
        fact=(1/sqrt(self.magnitudes[0]**2+self.magnitudes[1]**2+self.magnitudes[2]**2))
        print(fact)
        self.magnitudes = [mag*fact for mag in self.magnitudes]
        print("DONE")
    def set(self,p):
        self.pts[0],self.pts[1]=p[0],p[1]
        self.normalize()
        self.angles=return_angles(self.magnitudes)
    def scale(self,fact):
        self.pts[0].scale(fact)
        self.pts[1].scale(fact)
        # return line(self.pts)

    
    def out(self):
        p1o,p2o=self.pts[0].out(),self.pts[1].out()
        return "\n  Line\n      magnitude (%s,%s,%s)"%(self.magnitudes[0],self.magnitudes[1],self.magnitudes[2])+"\n        Endpts[ "+p1o+' -> '+p2o+' ]'
def cross(b,a):
    print("LINE CROSS")
    x,y,z = b.magnitudes[0],b.magnitudes[1],b.magnitudes[2]
    ax,ay,az = a.magnitudes[0],a.magnitudes[1],a.magnitudes[2]
    print(x,y,z,ax,ay,az)
    print(y*az-z*ay,x*az-z*ax,x*ay-y*ax)
    mag = Point3([y*az-z*ay , -(x*az-z*ax), x*ay-y*ax])
    print(mag.x,mag.y,mag.z)
    cross = Vec3(mag)
    print(len(cross.lines))
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

        #put in tuple - connect them all
        self.lines = [[],[]]
        if type(p1)==list:
            if type(p1[0])==float and len(p1)==3:
                p1=Point3(p1)
                l=line([Point3([0.,0.,0.]),p1])
                self.lines[0]=[l]
            if type(p1[0]) == Point3:
                if len(p1)==2:
                    l = line(p1)  
                    self.lines[0]=[l]
                else:
                    print('handling list of pts greater than 2')
                    count=0
                    lastpt=p1[0]
                    for pt in p1:
                        if count==0:
                            lastpt=pt
                            count+=1
                        if count==1:
                            l=line([lastpt,pt])
                            self.lines[0]=[l]
                            count+=1
                            lastpt=pt
                        if count==2:
                            l=line([lastpt,pt])
                            self.lines[1]=[l]
                            count+=1
                            lastpt=pt
                        else:
                            l=line([lastpt,pt])
                            self.lines+=[l]
                            count+=1
                            lastpt=pt
        else:
            if type(p1)==Point3:
                print('else')
                l=line(p1)
                print(l.out())
                self.lines[0]=l
                                        #last point in last line, first point in first line
        self.head=Point3()
        self.tail=Point3()
        self.head_magnitude = [self.head.x-self.tail.x,self.head.y-self.tail.y,self.head.z-self.tail.z]
        self.dir_vector = [0.,0.,0.]
        self.check_vec()
        self.update_vector()

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
            return Vec3([self.head.x-a.head.x, self.head.y-a.head.y, self.head.z-a.head.z])
        else:
            print("invalid")

    # def cross(self,a,b=None):
    #     print("VEC3 CROSS")
    #     if b==None:
    #         return Vec3([self.y*a.head.z-self.z*a.head.y , -(self.head.x*a.head.z-self.z*a.head.x), self.head.x*a.head.y-self.y*a.head.x])
    #     else:
    #         if type(b) == list:
    #             return Vec3([a.head.y*b[3]-a.head.z*b[2] , -(a.head.x*b[3]-a.head.z*b[1]), a.head.x*b[2]-a.head.y*b[1]])
    #         elif type(b) == Vec3:
    #             return Vec3([a.head.y*b.z-a.head.z*b.y , -(a.head.x*b.z-a.head.z*b.x), a.head.x*b.y-a.head.y*b.x])
    #         else:
    #             print("invalid")
    def dot(self,a,b=None):
        if b==None:
            return a.head.x*self.head.x+a.head.y*self.y+a.head.z*self.z
        else:
            if type(b) == list:
                return a.head.x*b[1]+a.head.y*b[2]+a.head.z*b[3]
            elif type(b) == Vec3:
                return a.head.x*b.x+a.head.y*b.y+a.head.z*b.z
            else:
                print("invalid")
                return None
    def scale_by_matrix(self, mat3):
        # MULTIPLIES A Vec3 OBJECT WITH Mat3 OBJECT AND RETURNS A NEW Vec3 
        x = self.head.x * mat3.matrix[0][0] + self.head.y * mat3.matrix[0][1] + self.head.z * mat3.matrix[0][2]
        y = self.head.x * mat3.matrix[1][0] + self.head.y * mat3.matrix[1][1] + self.head.z * mat3.matrix[1][2]
        z = self.head.x * mat3.matrix[2][0] + self.head.y * mat3.matrix[2][1] + self.head.z * mat3.matrix[2][2]
        return Vec3(x, y, z)
    def scale_by_factor(self, fact):
        # MULTIPLIES A self OBJECT WITH Mat3 OBJECT AND RETURNS A NEW self 
        print("SCALING")
        li=[]
        for l in self.lines:
            pts = [Point3([l.pts[0].x*fact,l.pts[0].y*fact,l.pts[0].z*fact]),
                    Point3([l.pts[1].x*fact,l.pts[1].y*fact,l.pts[1].z*fact])]
            li.append(line(pts))
        self.lines=[] 
        for l in li:
            self.lines.append(l)
        self.head = self.lines[-1].pts[1]
        self.tail = self.lines[0].pts[0]
        if type(self.head) ==Point3 and type(self.tail) == Point3:
            self.head_magnitude=[self.head.x-self.tail.x,self.head.y-self.tail.y,self.head.z-self.tail.z] 
        self.check_vec()
        self.out_all()
    def ret_magnitude(self):
        return hypot(self.head.x,self.head.y,self.head.z)
    def out_head(self):
        return '\nHead of vector: \n'+line(self.ret_tail_head()).out()+'\n'
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
        print("NORMALIZING")
        fact=(1/sqrt(self.head_magnitude[0]**2+self.head_magnitude[1]**2+self.head_magnitude[2]**2))
        print(fact)
        norm = self.scale_by_factor(fact)
        print("DONE")
        return norm
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
                    print(type(l))
                    l.append(self.lines[count])
                    count+=1
        # print(indexes)
        # print(ind)
        self.lines = []
        for every in l:
            self.lines.append(every)

    def ret_tail_head(self):
        if len(self.lines)==1:
            return [self.lines[0].pts[0],self.lines[0].pts[1]]
        print(len(self.lines))
        return [self.lines[0].pts[0],self.lines[-1].pts[1]]
    def update_vector(self):
        x,y,z=0.,0.,0.
        for l in self.lines:
            x+=l.magnitudes[0]
            y+=l.magnitudes[1]
            z+=l.magnitudes[2]
        self.head_magnitude = [x,y,z]

def make_vector(p1,p2=None):
    if p2==None:
        return Vec3(p1)
    else:
        v0,v1 = Vec3(p1),Vec3(p2)
        return v1.sub(v0)

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

def normal_vec(square):
    print("NORMAL VECTOR")

    if type(square)==Vec3:
        if len(square.lines)>2:
            norm=Vec3(cross(square.lines[0],square.lines[1]))
            print("NORMALIZING")
            fact=(1/sqrt(norm.head_magnitude[0]**2+norm.head_magnitude[1]**2+norm.head_magnitude[2]**2))
            print("factor "+str(fact))
            norm.scale_by_factor(fact)
            print("DONE w NORMAL VECTOR")
            print(norm.out_all())
            return norm
        else:
            norm=Vec3([0.,0.,0.])


def scale_by_matrix(line, mat3):
    # MULTIPLIES A Vec3 OBJECT WITH Mat3 OBJECT AND RETURNS A NEW Vec3 
    p1,p2=line.pts[0],line.pts[1]
    p1.set([p1.x * mat3.matrix[0][0] + p1.y * mat3.matrix[0][1] + p1.z * mat3.matrix[0][2],
            p1.x * mat3.matrix[1][0] + p1.y * mat3.matrix[1][1] + p1.z * mat3.matrix[1][2],
            p1.x * mat3.matrix[2][0] + p1.y * mat3.matrix[2][1] + p1.z * mat3.matrix[2][2]])

    p2.set([p2.x * mat3.matrix[0][0] + p2.y * mat3.matrix[0][1] + p2.z * mat3.matrix[0][2],
            p2.x * mat3.matrix[1][0] + p2.y * mat3.matrix[1][1] + p2.z * mat3.matrix[1][2],
            p2.x * mat3.matrix[2][0] + p2.y * mat3.matrix[2][1] + p2.z * mat3.matrix[2][2]])
class Transform:
    # IT TRANSFORMS THE X AND Y FROM NORMALIZED SPACE TO SCREEN SPACE WITH PROJECTION APPLIED
    def worldSpaceTransform(self, vec3, w, h):
        if vec3.z == 0:
            vec3.z = 0.001
        zInverse = 1/ vec3.z
        xTransformed = ((vec3.x * zInverse) + 1) * (w/2)
        yTransformed = ((-vec3.y * zInverse) + 1) * (h/2)
        xTransformed = str(xTransformed)[:6]
        yTransformed = str(yTransformed)[:6]
        return Vec2(float(xTransformed), float(yTransformed))

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


class Square:
    def __init__(self,pts):
        self.rotator = Rotation()
        self.transform = Transform()
        
        self.endpoints=pts
        self.square_vec=Vec3(pts)
        self.current_rotation=[0.,0.,0.]
        self.normal_vector = normal_vec(self.square_vec)
        print("SQUARE NORMAL :")
        print(self.normal_vector.lines)


    def out(self):
        print("SQUARE")
        print("\nnormal vector: "+self.normal_vector.lines[0].out())
        return self.square_vec.out_all(square=True)

    def rotate(self,rotations):
        # ROTATES A Vec3 (a) BY GIVEN THETA AND AXIS
        
        current_rotation=[0.,0.,0.]
        theta,eta,phi=rotations[0],rotations[1],rotations[2]

        # mx,my,mz = rotateX(theta)
        if theta != 0:
            current_rotation[0]=theta
            for l in self.square_vec.lines:
                scale_by_matrix(l, rotateX(theta))
        if eta != 0:
            current_rotation[1]=eta
            for l in self.square_vec.lines:
                scale_by_matrix(l, rotateY(eta))
        if phi !=0 :
            current_rotation[2]=phi
            for l in self.square_vec.lines:
                scale_by_matrix(l, rotateZ(phi))

        self.endpoints=[self.square_vec.lines[0].pts[0],self.square_vec.lines[1].pts[0],
                        self.square_vec.lines[2].pts[0], self.square_vec.lines[3].pts[0]]
        self.normal_vector = normal_vec(self.square_vec)
        return self.current_rotation
    # def update(self):

    def intersect_with(self,muon, epsilon=1e-6):
        """
        p0, p1: Define the line.
        p_co, p_no: define the plane:
            p_co Is a point on the plane (plane coordinate).
            p_no Is a normal vector defining the plane direction;
                (does not need to be normalized).

        Return a Vector or None (when the intersection can't be found).
        """


        line = muon.track
        dot = self.normal_vector.dot(line)

        if abs(dot) > epsilon:
            # The factor of the point between p0 -> p1 (0 - 1)
            # if 'fac' is between (0 - 1) the point intersects with the segment.
            # Otherwise:
            #  < 0.0: behind p0.
            #  > 1.0: infront of p1.
            w = make_vector(self.origin,muon.track.tail)
            fac = -self.normal_vector.dot(w) / dot
            line = line.scale_by_factor(fac)

            boundy,boundz = [0.,0.],[0.,0.]
            for endpt in self.endpoints:
                if endpt.y > boundy[2]:
                    boundy[2] = endpt.y
                if endpt.y < boundy[1]:
                    boundy[1] = endpt.y

                if endpt.z > boundz[2]:
                    boundz[2] = endpt.z
                if endpt.z < boundz[1]:
                
                    boundz[1] = endpt.z
                
            if line[1].y > boundy[2] or line[1].y < boundy[1] or line[1].z > boundz[2] or line[1].z < boundz[1]:
                print("outside chamber")
                return None
            else:
                print("intersection found at: ")
                return muon.hit.add(line[1])
        else:
            # The segment is parallel to plane.
            print("parralell")
            return None

# p4 = Point3([-4.,0.,4.])
# p3 = Point3([9.,-3.,-1.])
# p2 = Point3([5.,3.,4.])
# p1 = Point3([1.,1.,1.])
# v=Vec3([p1,p2,p3,p4])
# print(v.out_all())
# f=5
# v.scale_by_factor(f)
# print(v.out_all)
