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
        print("    Calculating Residuals")
        # residual = self.get_residuals(track_slope,hit)
        self.translate(Point3([5.,0.,0.]))
        # print(self.endpoints)
        time.sleep(1)
    # def get_residuals(self,track_slope,des_hit,act_hit):
    #     residual_y=des_hit.y-act_hit.y
    #     residual_x=des_hit.x-act_hit.x
    #     x_steps = [-stepSizes[0], 0, stepSizes[0]]
    #     y_steps = [-stepSizes[1], 0, stepSizes[1]]
    #     z_steps = [-stepSizes[1], 0, stepSizes[1]]
    #     theta_steps = [-stepSizes[2], 0, stepSizes[2]]
    #     eta_steps = [-stepSizes[2], 0, stepSizes[2]]
    #     phi_steps = [-stepSizes[2], 0, stepSizes[2]]
    #     minValue = 1000
    #     lowesState = [0,0,0]
    #     noDisValue = 0
    #     xSTD = []
    #     for x_dis in x_steps:
    #         for y_dis in y_steps:
    #             for z_dis in z_steps:
    #                 for t_dis in theta_steps:
    #                     for e_dis in eta_steps:
    #                         for p_dis in phi_steps:
    #                             predictedResidual =  y_dis - track_slope[1]*z_dis - act_hit.y*track_slope[1]*t_dis + act_hit.x*track_slope[1]*e_dis+act_hit.x*p_dis
    #                             squaredDifference = np.power(predictedResidual - residual_y,2)
    #                             squaredDifference = squaredDifference[~np.isnan(squaredDifference)]
    #                             stdDev = np.mean(squaredDifference)
    #                             if stdDev < minValue and not (x_dis == 0 and y_dis == 0 and t_dis ==0):
    #                                 lowesState = [x_dis,y_dis, t_dis]
    #                                 minValue  = stdDev
    #                             if x_dis == 0 and y_dis == 0 and t_dis ==0:
    #                                 noDisValue = stdDev
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