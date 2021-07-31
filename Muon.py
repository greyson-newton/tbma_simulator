from geometry import *

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
