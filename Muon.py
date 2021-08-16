from geometry import *
from math import pi
import random

# be an implementation of a Vector3
class Muon:
    def __init__(self,first_hit=None):   #takes
        self.track=Vec3(zero_pt)
        if first_hit!= None:
           self.track=Vec3(Point3([first_hit.z,first_hit.y,first_hit.x]))

        self.path=Vec3(zero_pt)
        self.typicalScatteringDistance = 10
        self.angleConstant = 40
        self.speedDecreaseConstant = .95
        self.magneticField = .2
        self.massOverCharge = 1.0
        self.pi = pi
        self.trac_hit=Vec3(zero_pt)
        self.scatter_hit=Vec3(zero_pt)
        self.track.check_vec()
    def propagate(self,p_f):
        print("    ----Muon Track Propagation----")
        self.p_f=p_f
        self.track=Vec3(Point3([p_f.x,p_f.y,p_f.z]))
        self.track.check_vec()
        print("    ",self.track.pts[0].out(), " -> ", self.track.pts[-1].out())
        print("    ----End Muon Track Propagation----\n")
    def scatteringDistance(self):
        scatteringDistance =  self.typicalScatteringDistance/(10*random.random() )
        return scatteringDistance

    def scatteringAngle(self,speed):
        sigma = self.angleConstant/(speed)
        deltaAngle = sigma*2*(.5-random.random())
        return deltaAngle
    def scatteringSpeed(self,speed,angle):
        speed = self.speedDecreaseConstant*speed*cos(angle)
        return speed
    def scatter(self):
        while self.path.pts[-1].x<self.p_f.x:
            pathLength = self.scatteringDistance()
            deltaAngle = self.scatteringAngle(self.speed)
            x = pathLength+self.path.pts[-1].x
            z = self.path.pts[-1].z+cos(self.currentAngle)*pathLength
            y = self.path.pts[-1].y+sin(self.currentAngle)*pathLength
            self.path.__add__(Point3(x,y,z))
        #if nextXPosition > xBound[1]:
        #    pathLength = (xBound[1]-xPositions[-1])/math.cos(currentAngle)
        #    nextXPosition = xBound[1]
        #    nextYPosition = yPositions[-1]+math.sin(currentAngle)*pathLength

        self.currentAngle = self.currentAngle + deltaAngle
    def plot_path(self):
        x,y,z=[],[],[]  
        for pt in self.path.pts:
            x.append(pt.z)
            y.append(pt.y)
            z.append(pt.x)
        return [x,y,z]
    def plot_pts(self):
        x,y,z=[],[],[]  
        for pt in self.track.pts:
            # print(pt.out())
            x.append(pt.z)
            y.append(pt.y)
            z.append(pt.x)
        return [x,y,z]
    #  VERBATUM FROM iterateMuon class, needs to be implemented into muon class
    # def iterateMuon(angleInitial, speed, charge, xInitial, yInitial):
    #     #radiusOfCurvature = massOverCharge*speed/magneticField #negative means curve the other way
    #     radiusOfCurvature = returnRadiusOfCurvature(massOverCharge, speed, magneticField)

    #     #flip y by charge, then flip back
    #     yInitial = yInitial*charge

    #     x0, y0 = circleFromPointAndRadius(xInitial, yInitial, radiusOfCurvature, angleInitial)

    #     #calculate scattering distance:
    #     distance = scatteringDistance()

    #     circumference = 2*pi*abs(radiusOfCurvature)

    #     if distance > circumference:
    #         distance = -999
    #         xFinal, yFinal, angleFinal = xInitial, yInitial, angleInitial
    #         angleAfterScatter = angleInitial
    #     else:
    #         angleCovered = distance/circumference*2*pi #angles are radians
    #         angleFinal = angleInitial + angleCovered

    #         xFinal, yFinal = circleFromPointAndRadius(x0,y0, -radiusOfCurvature, angleFinal)

    #         scatAngle = scatteringAngle(speed)
    #         angleAfterScatter =  angleFinal + scatAngle

    #         speed = scatteringSpeed(speed,scatAngle)

    #     if xFinal < xInitial:
    #         distance = -999

    #     #flip y by charge, then flip back
    #     yFinal = yFinal*charge
