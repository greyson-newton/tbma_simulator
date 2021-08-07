from logging import RootLogger

from matplotlib.cbook import pts_to_midstep
from geometry import *
import math
import matplotlib.pyplot as plt
import time
from mpl_toolkits import mplot3d
class Chamber:
    def __init__(self,dim,origin,rotation,actual=None):
        if actual==None:
            self.design=True
        else:
            self.design=False
        self.w,self.h = dim[0],dim[1]
        self.origin=origin
        self.rotation=rotation
        self.current_rotation=rotation
        x,y,z,w,h = self.origin.x,self.origin.y,self.origin.z,self.w,self.h
        self.endpoints=[Point3([x,y+h,z+w]),Point3([x,y+h,z-w]),Point3([x,y-h,z-w]),Point3([x,y-h,z+w]),Point3([x,y+h,z+w])]
        # for pt in self.endpoints:
        #     print(pt.out())
        self.square=Square(self.endpoints,self.origin)

        self.rotate(rotation)
        # self.translate(origin)
    def rotate(self,rotation):
    # def translate_by(self,translations):
    #     self.square = [Vec3.__add__(pt,t) for pt,t in self.plane]        
    # def rotate_by(self,rotations):

        self.current_rotation = self.square.rotate(rotation)
        self.endpoints=self.square.endpoints
    def translate(self,translation):
        # print("BEFORE TRANSLATION")
        # # print(translation.out())
        # for pt in self.endpoints:
        #     print("chamber endpts ",pt.out())
        # for pt in self.square.endpoints:
        #     print("square endpoints",pt.out())    
        self.square.translate(translation,self.design) 
        # for pt in self.endpoints:
        #     print("chamber ",pt.out())
            # pt.x+=translation.x
            # pt.y+=translation.y
            # pt.z+=translation.z
        # for pt in self.square.endpoints:
        #     print("square ",pt.out())
    
        self.endpoints=self.square.endpoints     
        self.origin=self.square.origin
        
         
        # print("AFTER TRANSLATION")
        # for pt in self.endpoints:
        #     print("chamber endpts ",pt.out())
        # for pt in self.square.endpoints:
        #     print("square endpoints",pt.out()) 
        
    def plot_pts(self):
        # print("plotting")

        x,y,z = [],[],[]
        for pt in self.endpoints:
            x.append(pt.x)
            y.append(pt.y)
            z.append(pt.z)
        return [x,y,z]
    def plot_vert(self):
        pts=self.endpoints
        verts=zip([pts[0].x,pts[0].y,pts[0].z],[pts[1].x,pts[1].y,pts[1].z],
                [pts[2].x,pts[2].y,pts[2].z],[pts[3].x,pts[3].y,pts[3].z])
        return verts
    def intersect(self,muon_vec):
        return self.square.intersect_with(muon_vec,self.origin)
    def align(self):
        self.translate(Point3([5.,0.,0.]))
        # print(self.endpoints)
        time.sleep(1)

            # def init(self,translations,rotations):
    #     self.rotate_by(rotations)
    #     self.translate_by(translations)
    #     self.bounds
# ax.plot([0, 0], [0, 0], [0, 10])  # extend in z direction
# ax.plot([0, 0], [0, 8], [0, 0])   # extend in y direction
# ax.plot([0, 9], [0, 0], [0, 0])   # extend in x direction
    # def move(self,translations,rotations):
    #     self.rotate_by(rotations)
#     #     self.translate_by(translations)
# from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# fig, ax = plt.subplots()
# plt.rcParams["figure.figsize"] = [6, 10]
# ax = plt.axes(projection='3d')  # set the axes for 3D plot
# ax.set_autoscale_on=True
# ax.set_xlim([-10, 10])
# ax.set_ylim([-10, 10])
# ax.set_zlim([-10, 10])

# dim = [5,5]
# origin=Point3()

# rotation=[0. ,0.,0.]
# translation=[5,0.,.0]
# chamber = Chamber(dim,origin,rotation)
# rotation=[0.,0.,1.]
# print("num lines")
# print(len(chamber.square.square_vec.lines))
# print(type(chamber.plot_pts()[0][0]))


# chamber.rotate(rotation)
# # ax.plot(chamber.plot_pts()[2],chamber.plot_pts()[1],chamber.plot_pts()[0])
# ax.plot(chamber.plot_pts()[0],chamber.plot_pts()[1],chamber.plot_pts()[2])
# chamber.translate(translation)
# ax.plot(chamber.plot_pts()[0],chamber.plot_pts()[1],chamber.plot_pts()[2])

# # print(chamber.square.out())
# # plt.plot(chamber.plot_pts())
# plt.show()