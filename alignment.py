from random import random
from pandas import DataFrame
from math import cos,sin,sqrt,pi,sqrt, tan
import numpy as np
#https://developer.rhino3d.com/guides/rhinopython/python-rhinoscriptsyntax-introduction/
from math import sin, cos, radians
# References
# powerful-python-tricks-data-science      
#       https://www.analyticsvidhya.com/blog/2019/08/10-powerful-python-tricks-data-science/
# maximizing-efficiency      
#       https://towardsdatascience.com/maximizing-efficiency-in-python-six-best-practices-for-implementing-python3-7-in-production-beadc226699
# python-memory-management
#       https://realpython.com/python-memory-management/
#timeit.timeit(listComp_square, number = 1000)
#       https://www.guru99.com/timeit-python-examples.html#:~:text=Python%20timeit%20%28%29%20is%20a%20method%20in%20Python,helps%20in%20checking%20the%20performance%20of%20the%20code.

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

class Muon:
    def __init__(self):   #takes
        self.track=[Vec3(0.,0.,0.,),Vec3(0.,0.,0.,)]
        self.path=[Vec3(0.,0.,0.,),Vec3(0.,0.,0.,)]

        self.typicalScatteringDistance = 10
        self.angleConstant = 40
        self.speedDecreaseConstant = .95
        self.magneticField = .2
        self.massOverCharge = 1.0
        self.pi = pi
    def propagate(self,p_f,speed,charge):
        self.track=[self.track[0],p_f]
    def scatter(self):
        self.path=[]


class alignment:
    def __init__(self):
        self.isDone=False
    def init_simulation(self):
        
        self.muons_per_blast = 10000
        self.muon = Muon()
        #chamber positioning
        self.design_center,self.design_rotation= Vec3(.0,.0,.0),[0.,0.,0.]
        self.actual_center,self.actual_rotation = Vec3(.0,.0,.0), [0.,0.,0.]
        #chamber sizing
        self.width,self.height = 0.,0.
        self.design_plane=[Vec3(.0,.0,.0),Vec3(.0,.0,.0),Vec3(.0,.0,.0),Vec3(.0,.0,.0)]
        self.actual_plane=[Vec3(.0,.0,.0),Vec3(.0,.0,.0),Vec3(.0,.0,.0),Vec3(.0,.0,.0)]
        #simulation parameters
        self.momentum_option, self.momentum,self.accuracuy = '',0., 0.   
        #geometry management

        
    def fill_sim_data(self,data): #Graphic Remote
        #
        self.design_ctr_pt=Vec3(float(data[0]),float(data[1]),float(data[2]))
        self.des_rotation=[float(data[3]),float(data[4]),float(data[5])]
        self.misalignment_shift =Vec3(float(data[6]),float(data[7]),float(data[8]))
        self.misalignment_rotation =[float(data[9]),float(data[10]),float(data[11])]
        self.width,self.height = data[12], data[13]
        self.momentum_option, self.accuracuy = data[14], data[15]
        if self.momentum_option == "AUTO":
            self.momentum = (self.design_ctr_pt[0]/30.)
        w,h= self.width/2,self.height/2

        self.des_plane = [Vec3(0.,h,w),Vec3(0.,h,-w),Vec3(0.,-h,w),Vec3(0.,-h,-w)]

        self.design_chamber=Chamber(self.des_plane)
        self.actual_chamber=Chamber(self.des_plane)

        #need to be in radians?
        self.design_chamber.rotate(self.des_rotation)
        self.actual_chamber.rotate(self.des_rotation+self.misalignment_rotation) 

        #translate
        self.design_chamber.translate(self.design_ctr_pt)
        self.actual_chamber.translate(self.design_ctr_pt+self.misalignment_shift)

    def simulate(self,plotter):
        for i in range(400):
            if self.isDone: #and self.chamber2.isDone() and self.chamber3.isDone()
                break

            plotter.updateEndpoints(self.actualEndpoints, self.designEndpoints)
            plotter.updateResidualPlot(self.chamber.returnResidual())
            plotter.updateLinePlots(self.chamber.countZ, self.chamber.countY, self.chamber.countP)
            
            self.shootMuons(self.chamber, plotter)

            self.chamber.align()
            self.chamber.resetData()

            plotter.resetEndpoints()
            plotter.resetLinePlot()
    def shootMuons(self):
        for i in range(self.muons_per_blast):
            if i%1000==0: print(i*1.0/self.muons_per_blast)

            #set up inital state of muon
            speedInitial = 1000
            charge = random.random()
            if charge > .5: charge = 1
            else: charge = -1
            
            self.muon.propagate(self.ret_random_design_hit(),speedInitial,charge)
            #make a class intersect? Or method in muon or chamber?
            intersect(self.muon.track,self.design_chamber.plane)

    def ret_random_design_hit(self):
        # center of the circle (x, y)
        circle_y = self.design_ctr_pt[1]
        circle_z = self.design_ctr_pt[2]
        circle_r = sqrt(circle_z**2+circle_y**2)
        self.x_bound = [0,self.design_ctr_pt[x]]
        self.y_bound = [-circle_r,circle_r]
        self.z_bound = [-circle_r,circle_r]
        # random angle
        alpha = 2 * pi * random.random()
        # random radius
        r = circle_r * sqrt(random.random())
        # calculating coordinates
        z = r * cos(alpha) + circle_z
        y = r * sin(alpha) + circle_y
        return Vec3(self.design_ctr_pt[0],y,z)


    def update_actual_chamber(self,data) :
        self.actual_position[0],self.actual_position[1],self.actual_position[2]=float(data[0]),float(data[1]),float(data[2])
        self.actual_rotation[1],self.actual_rotation[1],self.actual_rotation[2]=float(data[3]),float(data[4]),float(data[5])
    def update_muon(self,data):
        self.muon_track,self.muon_path=data[0],data[1]
    def update_muon_plot(self):
        plotter.updateMuonPath()
        plotter.resetMuonPaths()




    def finalize_simulation(self):
        sim_outcomes = pd.DataFrame({'time to complete' : [0.] #time in sec?ms?
                            'algorithm params' : ['','','']  #accuracy of acceptance, nIterations to achieve acc, momentum,
                            'final position' : [0.,0.,0.,0.,0.,0.],
                            'design position' : [0.,0.,0.,0.,0.,0.],
                            'difference' : [0.,0.,0.,0.,0.,0.],
                            'chamber size' : [0.,0.],                   #w,h   
                            })  
        alignmentReport.report(sim_outcomes)
    def terminate_sim(self):
        self.finalize_simulation()
        self.init_simulation()
    def actual_chamber_pos(self):
        return [self.width,self.height]
    def full_chamber_distance(self,dir):
        return 