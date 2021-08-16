# https://stackoverflow.com/questions/8963082/how-to-update-a-matplotlib-figure-from-a-function-in-a-qt-gui
from random import random
from pandas import DataFrame
from math import cos,sin,sqrt,pi,sqrt, tan
import numpy as np
#https://developer.rhino3d.com/guides/rhinopython/python-rhinoscriptsyntax-introduction/
from math import sin, cos, radians
from Muon import *
from chamber import *
from geometry import *
from pylab import *
# import time

# ion()

# References
# powerful-python-tricks-data-science      
#       https://www.analyticsvidhya.com/blog/2019/08/10-powerful-python-tricks-data-science/
# maximizing-efficiency      
#       https://towardsdatascience.com/maximizing-efficiency-in-python-six-best-practices-for-implementing-python3-7-in-production-beadc226699
# python-memory-management
#       https://realpython.com/python-memory-management/
#timeit.timeit(listComp_square, number = 1000)
#       https://www.guru99.com/timeit-python-examples.html#:~:text=Python%20timeit%20%28%29%20is%20a%20method%20in%20Python,helps%20in%20checking%20the%20performance%20of%20the%20code.



class alignment:
    def __init__(self,data) :
        # self.fig, self.ax = plt.subplots()
        # plt.rcParams["figure.figsize"] = [6, 10]
        # self.ax = plt.axes(projection='3d')  # set the axes for 3D plot


        self.isDone=False
        self.crnt_rotation=[0.,0.,0.]
        self.muons_per_blast = 10
        

        self.actual_center,self.actual_rotation=[],[]

        self.design_center = Point3([float(data[0]),float(data[1]),float(data[2])])
        shift = Point3([float(data[6]),float(data[7]),float(data[8])])
        self.design_rotation = Point3([float(data[3]),float(data[4]),float(data[5])])
        rot = Point3([float(data[9]),float(data[10]),float(data[11])])


        self.actual_rotation=self.design_rotation.add(rot)
        self.actual_center=self.design_center.add(shift)
        self.dimensions = [float(data[12]), float(data[13])]
        self.momentum_option, self.accuracuy = str(data[14]), float(data[15])

        if self.momentum_option == "AUTO":
            self.momentum = float(self.design_center.x/30.)

        self.bounds=[dim/2. for dim in self.dimensions]
        self.muon = Muon(self.design_center)
        self.design_chamber = Chamber(self.bounds,self.design_center,self.design_rotation)
        self.actual_chamber = Chamber(self.bounds,self.actual_center,self.actual_rotation,1)

# line1.axes.set_xlim(-10, 10)
# line1.axes.set_ylim(-2, 2)
# line1.set_label("line1")
# line2.set_label("line2")
# legend()
# grid()
# # draw()
#         self.design, =  self.ax.plot([], [], [], lw=2)
#         # self.ax.plot(self.muon.plot_track()[0],self.muon.plot_track()[1],self.muon.plot_track()[2])
#         self.actual, = self.ax.plot([], [], [], lw=2)

#         self.muon_track, =  self.ax.plot([], [], [], lw=2)
#         # self.ax.plot(self.muon.plot_track()[0],self.muon.plot_track()[1],self.muon.plot_track()[2])
#         self.muon_path, = self.ax.plot([], [], [], lw=2)
        # self.ax.plot(self.muon.plot_track()[0],self.muon.plot_track()[1],self.muon.plot_track()[2])
    def simulate(self):
        # if self.isDone: #and self.chamber2.isDone() and self.chamber3.isDone()
        print("Muon Blast Iteration")

        # plotter.updateEndpoints(self.actualEndpoints, self.designEndpoints)
        # plotter.updateResidualPlot(self.chamber.returnResidual())
        # plotter.updateLinePlots(self.chamber.countZ, self.chamber.countY, self.chamber.countP)
        print("-------BLASTING MUONS--------\n")
        a_h,d_h=self.shootMuons()
        # track_slope=self.return_slope_on_hit()
        if a_h and d_h:
            print("-------ALIGNING CHAMBERS--------\n")
            self.actual_chamber.align()    #needs to be implemented

            # self.actual_chamber.align(track_slope)    #needs to be implemented
        # self.actual = self.ax.plot(self.actual_chamber.plot_pts()[0],self.actual_chamber.plot_pts()[1],self.actual_chamber.plot_pts()[2])
        # self.fig.canvas.draw()
        # self.fig.canvas.flush_events()
    def shootMuons(self):
        
        # for i in range(self.muons_per_blast):
        self.muon.propagate(self.ret_random_design_hit())
        # if i%1000==0: 
        #     print(i*1.0/self.muons_per_blast)
        # self.muon_path.set_xdata(self.muon.plot_path()[0]) 
        # self.muon_path.set_ydata(self.muon.plot_path()[1])
        # self.muon_path.set_zdata(self.muon.plot_path()[2])
        # self.muon_track.set_xdata(self.muon.plot_track()[0]) 
        # self.muon_track.set_ydata(self.muon.plot_track()[1])
        # self.muon_track.set_zdata(self.muon.plot_track()[2])
        #set up inital state of muon
        speedInitial = 1000
        charge = random()
        if charge > .5: charge = 1
        else: charge = -1
        
        
        #make a class intersect? Or method in muon or chamber?
        d_h,a_h=False,False
        print("\n    ----Muon-Chamber Intersection----")
        print("    checking for design chamber hit w muon track")
        des_hit = self.design_chamber.intersect(self.muon)
        if des_hit!=None:
            if type(des_hit)==Point3:
                d_h=True
                print("    Muon track hit Design Chamber at: ", des_hit.out())
            else:
                print("    NOT POINT")
        else:
            print("    Muon track did not pass the design chamber")
        print("    checking for actual chamber hit w muon track")
        act_hit= self.actual_chamber.intersect(self.muon)
        if act_hit!=None:
            if type(act_hit)==Point3:
                a_h=True
                print("    Muon track hit Actual Chamber at: ", act_hit.out())       
            else:
                print("    NOT POINT")
        else:
            print("    Muon track did not pass actual chamber") 
        print("    ----End Muon-Chamber Intersection----\n")

        print("\n------------SIMULATION ITERATION RESULTS------------")
        if d_h and a_h:
            print("This iteration can be used")
            print("Muon-Track: ", self.muon.track.pts[-1].out())
            # print("Muon-Track: ", self.muon.track.pts[-1].out()," Muon-Path: ", self.muon.path.pts[-1].out())
            print("Design and Actual Muon-Track Hits: \n    Des:", des_hit.out(), "\n    Act:",act_hit.out())
            # print("Design & Actual Muon-Path Hits: ")
        else:
            print("This iteration unusable")
            
        print("\n------------SIMULATION ITERATION END------------\n")
        return a_h,d_h

    def ret_random_design_hit(self):
        circle_r = sqrt(self.bounds[0]**2+self.bounds[1]**2)
        # self.x_bound = [0,self.design_center.x]
        # self.y_bound = [-circle_r,circle_r]
        # self.z_bound = [-circle_r,circle_r]
        # random angle
        alpha = 2 * pi * random()
        # random radius
        r = circle_r * sqrt(random())
        # calculating coordinates
        z = r * cos(alpha) + self.design_center.z
        y = r * sin(alpha) + self.design_center.y
        p =Point3([self.design_center.x+r,y,z])
        # print(p.out())
        return p
    def return_slope_on_hit(self,p_intersection):
        # each meter has a femto-scaled num of points. 1e15. right now using arnd half-femto. 1e
        # 8
        track_dx_dz=(self.muon.track.pts[-1].x-self.muon.track.pts[0].x)/(self.muon.track.pts[-1].z-self.muon.track.pts[0].z)
        track_dy_dz=(self.muon.track.pts[-1].y-self.muon.track.pts[0].y)/(self.muon.track.pts[-1].z-self.muon.track.pts[0].z)
        return track_dx_dz,track_dy_dz
        # half_femto=10000000*(self.design_chamber.origin.x)
        # np.arange(self.track.pts[0].x,self.track.pts[-1].x,half_femto)
        # self.design_center = Vec3(float(data[0]),float(data[1]),float(data[2]))
        # self.actual_center = self.design_center.sub(Vec3(float(data[6]),float(data[7]),float(data[8])))
        # self.design_rotation = Point3([float(data[3]),float(data[4]),float(data[5])])
        # self.actual_rotation = self.design_rotation.add(Point3([float(data[9]),float(data[10]),float(data[11])]))

        
        # self.dimensions = [float(data[12]), float(data[13])]
        # self.momentum_option, self.accuracuy = str(data[14]), float(data[15])
# anim = []
# fig = plt.figure()
# matplotlib.interactive(True)
# ax = fig.add_subplot(111, projection='3d')
# design, =  ax.plot([], [], [], lw=2)
# # ax.plot(muon.plot_track()[0],muon.plot_track()[1],muon.plot_track()[2])
# actual, = ax.plot([], [], [], lw=2)

# muon_track, =  ax.plot([], [], [], lw=2)
# # ax.plot(muon.plot_track()[0],muon.plot_track()[1],muon.plot_track()[2])
# muon_path, = ax.plot([], [], [], lw=2)
from mpl_toolkits.mplot3d.art3d import Poly3DCollection,Line3DCollection
from mpl_toolkits.mplot3d import art3d
from matplotlib import cm
import numpy, weakref
ion()
fig = plt.figure(figsize=[30,26])
ax = fig.add_subplot(111, projection='3d')
data=[50.,0.,0.,0.,0.,0.,-20.,0.,0.,0.,0.,0.,10.,10.,"AUTO",.0000001]
tbma =alignment(data)

des_vertices = tbma.design_chamber.plot_pts()
act_vertices = tbma.actual_chamber.plot_pts()
# Initialize an object to concatentate all the face vertices
# poly_collection = None
# verts=list([des_vertices,act_vertices])
# # design = Poly3DCollection(des_vertices, alpha=0.8)
# # actual = Poly3DCollection(act_vertices, alpha=0.8)
# for l,s,m in zip(des_vertices[0],des_vertices[1],des_vertices[2]):
#     print("z ",l," y ", s," z ",m)
# https://mathematica.stackexchange.com/questions/189338/removing-some-of-the-box-in-a-plot3d
ax.set(xlabel ='Z-Axis', ylabel ='Y-Axis', zlabel='X axis',
       xlim =(-20,20), ylim =(-20, 20), zlim=(0, 60),
       title ='TBMA')
ax.get_xaxis().set_visible(False)
ax.get_zaxis().set_visible(True)

des=ax.plot_trisurf(des_vertices[2], des_vertices[1], des_vertices[0], cmap=cm.jet, linewidth=0.2,alpha=0.2)
act=ax.plot_trisurf(act_vertices[2], act_vertices[1], act_vertices[0], cmap=cm.magma, linewidth=0.2,alpha=0.4)
track =ax.plot(tbma.muon.plot_pts()[2], tbma.muon.plot_pts()[1], tbma.muon.plot_pts()[0],linewidth=1.)
print(type(des))
# pause(3)
for iteration in range(5):
    # act.pop(0).remove()
    # tbma.actual_chamber.rotate([45,0,0])
    # tbma.actual_chamber.rotate([0,0,45])
    tbma.simulate()
    # actual.cla()
    # track.cla()
    pause(2)    
    track.pop(0).remove()
    act_vertices=tbma.actual_chamber.plot_pts()
    # act.cla()
    act=ax.plot_trisurf(act_vertices[2], act_vertices[1], act_vertices[0], cmap=cm.magma, linewidth=0.2,alpha=0.4)
    track =ax.plot(tbma.muon.plot_pts()[0], tbma.muon.plot_pts()[1], tbma.muon.plot_pts()[2],linewidth=1.)
    draw()
savefig("tbma-v1.png")
# pc = art3d.Poly3DCollection( verts, facecolor='white', edgecolor='black', linewidths=0.05, alpha=1 )
# ax.add_collection( pc )
#     l = ax.lines.pop(0)
#     wl = weakref.ref(l)  # create a weak reference to see if references still exist
# #                      to this object
#     print wl  # not dead
#     l.remove()



# draw()
# pause(3)
# for iteration in range(2):
#     tbma.simulate()
#     # actual.cla()
#     # track.cla()
#     pause(2)
#     ax.cla()
#     ax.plot(tbma.actual_chamber.plot_pts()[0], tbma.actual_chamber.plot_pts()[1], tbma.actual_chamber.plot_pts()[2], color='b', alpha=0.5)
#     ax.plot(tbma.muon.plot_pts()[0], tbma.muon.plot_pts()[1], tbma.muon.plot_pts()[2], color='r', alpha=0.5)
#     draw()

    # for obj in [tbma.actual_chamber,tbma.muon]:
    #     ax.plot(obj.plot_pts()[0], obj.plot_pts()[1], obj.plot_pts()[2], color='b', alpha=0.5)
    #     plt.draw()
    #     plt.pause(2)
    #     ax.cla()
# ax.plot(tbma.muon.plot_track()[0], tbma.muon.plot_track()[1], tbma.muon.plot_track()[2], color='b', alpha=0.5)
# ax.plot(tbma.muon.plot_path()[0], tbma.muon.plot_path()[1], tbma.muon.plot_path()[2], color='b', alpha=0.5)
# plt.show()

# def init():
#     actual.set_data([], [])
#     actual.set_3d_properties([])
#     muon_path.set_data([], [])
#     muon_path.set_3d_properties([])
#     muon_track.set_data([], [])
#     muon_track.set_3d_properties([])
# def animate(ma):
#     print("animate")
#     ma.simulate()
#     actual = ax.plot(ma.actual_chamber.plot_pts()[0], ma.actual_chamber.plot_pts()[1], ma.actual_chamber.plot_pts()[2], color='b', alpha=0.5)
#     muon_track = ax.plot(ma.muon.plot_track()[0], ma.muon.plot_track()[1], ma.muon.plot_track()[2], color='b', alpha=0.5)
#     muon_path = ax.plot(ma.muon.plot_path()[0], ma.muon.plot_path()[1], ma.muon.plot_path()[2], color='b', alpha=0.5)
#     return [muon_track,actual,muon_path]
# for i in range(10):
#     plts =animate(tbma)
#     plt.draw()
#     for pl in plts:
#         for x in pl:
#             x.remove()
# anim.append(animation.FuncAnimation(fig, animate, init_func=init, fargs=(tbma),
#                         frames=10, interval=200,
#                         repeat_delay=5, blit=True))
    # def update_actual_chamber(self,data) :
    #     self.actual_position[0],self.actual_position[1],self.actual_position[2]=float(data[0]),float(data[1]),float(data[2])
    #     self.actual_rotation[1],self.actual_rotation[1],self.actual_rotation[2]=float(data[3]),float(data[4]),float(data[5])
    # def update_muon(self,data):
    #     self.muon_track,self.muon_path=data[0],data[1]
    # def update_muon_plot(self):
    #     plotter.updateMuonPath()
    #     plotter.resetMuonPaths()




    # def finalize_simulation(self):
    #     sim_outcomes = pd.DataFrame({'time to complete' : [0.] #time in sec?ms?
    #                         'algorithm params' : ['','','']  #accuracy of acceptance, nIterations to achieve acc, momentum,
    #                         'final position' : [0.,0.,0.,0.,0.,0.],
    #                         'design position' : [0.,0.,0.,0.,0.,0.],
    #                         'difference' : [0.,0.,0.,0.,0.,0.],
    #                         'chamber size' : [0.,0.],                   #w,h   
    #                         })  
    #     alignmentReport.report(sim_outcomes)
    # def terminate_sim(self):
    #     self.finalize_simulation()
    #     self.init_simulation()
    # def actual_chamber_pos(self):
    #     return [self.width,self.height]
    # def full_chamber_distance(self,dir):
    #     return 