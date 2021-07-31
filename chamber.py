from geometry import *

class Chamber:
    def __init__(self,plane):
        self.plane=plane
        self.transform =Transform()
        self.rotation =Rotation()
    def translate(self,translations):
        self.plane = [Vec3.__add__(pt,translations) for pt in self.plane]
    def rotate(self,rotations):
        #if looking down the x-axis (x is frozen)
        count=0
        #apply any angles
        for angle in rotations:
            if angle != 0.: #theres an angle involved
                if count==0: #theta rotation 
                    self.plane = [self.rotation.rotate(pt, angle, axis='x') for pt in self.plane]                                 
                    count+=1
                if count==1: #eta rotation 
                    self.plane = [self.rotation.rotate(pt, angle, axis='y') for pt in self.plane]                    
                    count+=1
                if count==2: #phi self.rotation
                    self.plane = [self.rotation.rotate(pt, angle, axis='z') for pt in self.plane]
                    count+=1
            else:
                count+=1
