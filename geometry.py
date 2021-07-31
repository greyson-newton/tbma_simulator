# 3X3 MATRIX INITIALIZED WITH ALL 0's
#https://developer.rhino3d.com/guides/rhinopython/python-rhinoscriptsyntax-introduction/
from math import sin, cos,sqrt,hypot
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

class Rotation: 

    def rotateX(self, theta):
        # ROTATION MATRIX IN X AXIS
        sinTheta = sin(theta)
        cosTheta = cos(theta)
        m = Mat3()
        m.matrix = [[1, 0,         0],
                    [0, cosTheta,  sinTheta],
                    [0, -sinTheta, cosTheta]]
        return m

    def rotate(self, vec3, theta, axis=None):
        # ROTATES A Vec3 BY GIVEN THETA AND AXIS
        if axis == "x":
            return multVecMatrix(vec3, self.rotateX(theta))
        if axis == "y":
            return multVecMatrix(vec3, self.rotateY(theta))
        if axis == "z":
            return multVecMatrix(vec3, self.rotateZ(theta))


#Make to be initialized empty,list,and another pt
class Point3(object):
    '''Creates a point on a coordinate plane with values x and y.'''

    COUNT = 0

    def __init__(self, p):
        # if p==None:
        #     self.x,self.y,self.z=0.,0.,0.
        #     self.pt=Point3([0.,0.,0.])
        # else:
        self.x, self.y,self.z = float(p[0]),float(p[1]),float(p[2])
        # self.pt=Point3(p)

    def add(self,p):   
        if type(p) == list:
            return Point3(self.x+p[0],self.y+p[1],self.z+p[2])
        elif type(p) == Point3:
            return Point3(self.x+p.x,self.y+p.y,self.z+p.z)
        else:
            print("invalid")
            return None
    def to_string(self):
        return "Point(%s,%s)"%(self.x,self.y,self.z) 
    def distance(self, p):
        dx,dy,dz = (self.x - p.x),(self.y - p.y),(self.z - p.z)  
        return sqrt(dx**2 + dy**2+dz**2)
    def to_vector(self,p=None):
        #from self.pt to the arbitrary Point3 p
        if p==None:
            return Vec3(self.pt)
        else:
            return Vec3(p).sub(Vec3(self.pt))
    def to_list(self):
        return [self.x, self.y,self.z]
    def out(self):
        return '('+str(self.x)+', '+str(self.y)+', '+str(self.z)+')'

class Vec2:
    # 2D VECTOR
    def __init__(self, x, y):
        self.x = x
        self.y = y
class Vec3:
    #  3D VECTOR
    def __init__(self,p1=None):
        if p1==None:
            self.magnitude,self.head,self.tail=0.,Point3(p1),Point3()
        else:
            if type(p1)==list:
                p1=Point3(p1)
            self.x,self.y,self.z=p1.x,p1.y,p1.z
            self.magnitude = hypot(p1.x,p1.y,p1.z)
            self.head,self.tail=Point3([p1.x,p1.y,p1.z]),Point3([0,0,0])

    def add(self,a, b=None):
        if b==None:
            return Vec3(a.x+self.x, a.y+self.y, a.z+self.z)
        else:
            if type(b) == list:
                return Vec3(a.x+b[0], a.y+b[1], a.z+b[2])
            elif type(b) == Vec3:
                return Vec3(a.x+b.x, a.y+b.y, a.z+b.z)
            else:
                print("invalid")
    def sub(self,a, b=None):
        if b==None:
            return Vec3([a.x-self.x, a.y-self.y, a.z-self.z])
        else:   
            if type(b) == list:
                return Vec3(a.x-b[0], a.y-b[1], a.z-b[2])
            elif type(b) == Vec3:
                return Vec3(a.x-b.x, a.y-b.y, a.z-b.z)
            else:
                print("invalid")
    def cross(self,a,b=None):
        if b==None:
            return Vec3(self.y*a.z-self.z*a.y , -(self.x*a.z-self.z*a.x), self.x*a.y-self.y*a.x)
        else:
            if type(b) == list:
                return Vec3(a.y*b[3]-a.z*b[2] , -(a.x*b[3]-a.z*b[1]), a.x*b[2]-a.y*b[1])
            elif type(b) == Vec3:
                return Vec3(a.y*b.z-a.z*b.y , -(a.x*b.z-a.z*b.x), a.x*b.y-a.y*b.x)
            else:
                print("invalid")
    def dot(self,a,b=None):
        if b==None:
            return a.x*self.x+a.y*self.y+a.z*self.z
        else:
            if type(b) == list:
                return a.x*b[1]+a.y*b[2]+a.z*b[3]
            elif type(b) == Vec3:
                return a.x*b.x+a.y*b.y+a.z*b.z
            else:
                print("invalid")
                return None
    def normalize(self):
        return self.vec*(1/sqrt(self.vec.x**2+self.vec.y**2+self.vec.z**2))
    def scale_by_matrix(self,vec3, mat3):
        # MULTIPLIES A Vec3 OBJECT WITH Mat3 OBJECT AND RETURNS A NEW Vec3 
        x = vec3.x * mat3.matrix[0][0] + vec3.y * mat3.matrix[0][1] + vec3.z * mat3.matrix[0][2]
        y = vec3.x * mat3.matrix[1][0] + vec3.y * mat3.matrix[1][1] + vec3.z * mat3.matrix[1][2]
        z = vec3.x * mat3.matrix[2][0] + vec3.y * mat3.matrix[2][1] + vec3.z * mat3.matrix[2][2]
        return Vec3(x, y, z)
    def scale_by_factor(self, fact):
        # MULTIPLIES A self OBJECT WITH Mat3 OBJECT AND RETURNS A NEW self 
        self.head.x = self.head.x * fact + self.head.y * fact + self.head.z * fact
        self.head.y = self.head.x * fact + self.head.y * fact + self.head.z * fact
        self.head.z = self.head.x * fact + self.head.y * fact + self.head.z * fact
        
    def ret_magnitude(self):
        return hypot(self.head.x,self.head.y,self.head.z)
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

def normal_vec(self,p1,p2,p3=None,p4=None):
    if type(p1)==Vec3 and type(p2)==Vec3:
        return p1.cross(p2)
    elif type(p3)==Point3 and type(p4)==Point3:
        v0,v1 = make_vector(p1,p2),make_vector(p3,p4)
        return v0.cross(v1)

class Plane3:
    def __init__(self,p1,p2,p3,p4,bounds,origin=None):

        transform = self.Transform()
        rotation = self.Rotation()

        if origin == None:
            self.origin,self.normal_vector= Point3(),Vec3()
        else:
            if type(p1)==Point3:
                self.normal_vector = normal_vec(p1,p2,p3,p4)
                self.normal_factor = self.coeff.dot(p1)
                # self.coeff*(x,y,z) = point

        def intersect_with(p0,p1, epsilon=1e-6):
            """
            p0, p1: Define the line.
            p_co, p_no: define the plane:
                p_co Is a point on the plane (plane coordinate).
                p_no Is a normal vector defining the plane direction;
                    (does not need to be normalized).

            Return a Vector or None (when the intersection can't be found).
            """
            line = make_vector(p0,p1)
            dot = self.normal_vector.dot(line)

            if abs(dot) > epsilon:
                # The factor of the point between p0 -> p1 (0 - 1)
                # if 'fac' is between (0 - 1) the point intersects with the segment.
                # Otherwise:
                #  < 0.0: behind p0.
                #  > 1.0: infront of p1.
                w = make_vector(self.origin,p0)
                fac = -self.normal_vector.dot(w) / dot
                line = line.scale_by_factor(fac)
                if abs(p1.y) > bounds.y and abs(p1.z) > bounds.z:
                    print("outside chamber")
                    return None
                else:
                    print("intersection found at: ")
                    return p0.add(line)
            else:
                # The segment is parallel to plane.
                print("parralell")
                return None

p1 = Point3([5,3,4])
p2 = Point3([1,1,1])

print(p1.x)
vector = Vec3(p1)

print(vector.head.out())
vector.scale_by_factor(3.3)
print(vector.head.out())
print(vector.magnitude)
print(make_vector(p1,p2).head.out())