from geometry import *
import math
import matplotlib.pyplot as plt

class Chamber:
    def __init__(self,dim,origin,rotation):
        self.w,self.h = dim[0],dim[1]
        self.origin=origin
        self.rotation=rotation
        self.current_rotation=rotation
        x,y,z,w,h = self.origin.x,self.origin.y,self.origin.z,self.w,self.h
        self.endpoints=[Point3([x,y+h,z+w]),Point3([x,y+h,z-w]),Point3([x,y-h,z-w]),Point3([x,y-h,z+w]),Point3([x,y+h,z+w])]
        self.square=Square(self.endpoints)

    def rotate(self,rotation_list):
    # def translate_by(self,translations):
    #     self.square = [Vec3.__add__(pt,t) for pt,t in self.plane]        
    # def rotate_by(self,rotations):

        self.current_rotation = self.square.rotate(rotation)
        self.endpoints=self.square.endpoints
    # def init(self,translations,rotations):
    #     self.rotate_by(rotations)
    #     self.translate_by(translations)
    #     self.bounds

    # def move(self,translations,rotations):
    #     self.rotate_by(rotations)
    #     self.translate_by(translations)
dim = [5,5]
origin=Point3()
rotation=[math.radians(45) ,0.,0.]
chamber = Chamber(dim,origin,rotation)

chamber.rotate()
print(chamber.square.out())
plt.plot(chamber.endpoints)