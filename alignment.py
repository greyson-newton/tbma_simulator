from random import random
from pandas import DataFrame
from math import cos,sin,sqrt,pi,sqrt, tan
import numpy as np
#https://developer.rhino3d.com/guides/rhinopython/python-rhinoscriptsyntax-introduction/
from math import sin, cos, radians
from Muon import *
from Chamber import *
from geometry import *
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
    def __init__(self):
        self.isDone=False
    def init_simulation(self):
        self.isDone=False
        
        self.muons_per_blast = 10000
        self.muon = Muon(self.muons_per_blast)

        self.bounds = [0.,0.]
        self.design_chamber = Chamber(self.bounds)
        self.actual_chamber = Chamber(self.bounds)

        
        #simulation parameters
        self.momentum_option, self.momentum,self.accuracuy = '',0., 0.   
        #geometry management

        
    def fill_sim_data(self,data): #Graphic Remote
        self.design_center = Vec3(float(data[0]),float(data[1]),float(data[2]))
        self.actual_center = self.design_center.sub(Vec3(float(data[6]),float(data[7]),float(data[8])))
        self.design_rotation = Point3([float(data[3]),float(data[4]),float(data[5])])
        self.actual_rotation = self.design_rotation.add(Point3([float(data[9]),float(data[10]),float(data[11])]))

        self.design_chamber.translate_by(self.design_center)
        self.actual_chamber.translate_by(self.actual_center)
        self.design_chamber.rotate_by(self.design_rotation)
        self.actual_chamber.rotate_by(self.actual_rotation)
        
        self.dimensions = [float(data[12]), float(data[13])]
        self.momentum_option, self.accuracuy = str(data[14]), float(data[15])

        if self.momentum_option == "AUTO":
            self.momentum = float(self.design_ctr_pt[0]/30.)

        self.bounds=[dim/2. for dim in self.dimensions]

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