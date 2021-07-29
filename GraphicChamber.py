from geometry import *
from constants import *
from numba import jit
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import math, time


class chamber:
    def __init__(self, idNumber, length, designX, designY, designAngle, actualX, actualY, actualAngle, accuracy, stepSizes):
        self.id = idNumber
        self.length = length
        self.accuracy = accuracy
        self.DONE = False
        self.time = 0
        self.stdDeviation = 0

        self.designAngle = designAngle
        self.designX = designX
        self.designY = designY
        self.designEndpoints = [[self.designX-self.length/2*math.cos(self.designAngle),self.designX+self.length/2*math.cos(self.designAngle)],[self.designY-self.length/2*math.sin(self.designAngle),self.designY+self.length/2*math.sin(self.designAngle)]]
        self.actualAngle = actualAngle
        self.actualX = actualX
        self.actualY = actualY
        self.actualEndpoints = [[self.actualX-self.length/2*math.cos(self.actualAngle),self.actualX+self.length/2*math.cos(self.actualAngle)],[self.actualY-self.length/2*math.sin(self.actualAngle),self.actualY+self.length/2*math.sin(self.actualAngle)]]

        self.hit = [[],[]]
        self.hitXOverY = []

        self.track = [[],[]]
        self.trackXOverY = []
        self.stepSizes = stepSizes
        self.countX, self.countY, self.countZ = 2, 2, 2
        self.alignStep  = [self.stepSizes[self.countX],self.stepSizes[self.countY],self.stepSizes[self.countZ]]

        self.fitness = []
        self.residualY = []
        self.predictedResidual = []

    def getResiduals(self, muonTrack, muonPath):
        #find predicted hit i.e. "track"

        interceptTrack = intersectAndHit(self.designEndpoints, muonTrack)

        #did it hit the chamber
        track =False
        minVal, maxVal = min(self.designEndpoints[1]), max(self.designEndpoints[1])
        if interceptTrack[1] < maxVal and interceptTrack[1] > minVal:
            track = True

        #find local dy/dx
        trackSlope = returnLocalDxDy(self.designAngle, muonTrack)
        transformedInterceptTrack = transformCord(self.designX, self.designY, self.designAngle, interceptTrack)
        #now, lets find the actual hit:
        hit = False
        for index, point in enumerate(muonPath[0]):
            if index == 0: continue
            segment = [[muonPath[0][index-1], muonPath[0][index]], [muonPath[1][index-1], muonPath[1][index]]]
            interceptHit  = intersectAndHit(self.actualEndpoints, segment)
            #did it hit the chamber
            minVal, maxVal = min(self.actualEndpoints[1]), max(self.actualEndpoints[1])
            if interceptHit[1] < maxVal and interceptHit[1] > minVal:
                hit = True
            if hit: 
                hitSlope = returnLocalDxDy(self.actualAngle, segment)
                transformedInterceptHit = transformCord(self.actualX, self.actualY, self.actualAngle, interceptHit)
                break

        if hit and track:
            self.hit[0].append(transformedInterceptHit[0])
            self.hit[1].append(transformedInterceptHit[1])
            self.hitXOverY.append(hitSlope)
            self.track[0].append(transformedInterceptTrack[0])
            self.track[1].append(transformedInterceptTrack[1])
            self.trackXOverY.append(trackSlope)

    def resetData(self):
        #print "design after align",  self.designX, self.designY, self.designAngle, self.designEndpoints
        self.hit = [[],[]]
        self.hitXOverY = []

        self.track = [[],[]]
        self.trackXOverY = []

    def align(self):

        hitY = np.asarray(self.hit[1])
        trackY = np.asarray(self.track[1])  
        dxdyTrack = np.asarray(self.trackXOverY)
        self.residualY = trackY-hitY
        print("Indices: ", self.countX, self.countY, self.countZ)
        self.alignStep  = [self.stepSizes[self.countX],self.stepSizes[self.countY],self.stepSizes[self.countZ]]
        print("AlignSteps: ", self.alignStep)
        possibleXDisplacements = np.linspace(-self.alignStep[0],  self.alignStep[0], 10)
        possibleYDisplacements = np.linspace(-self.alignStep[1], self.alignStep[1], 10)
        possibleAngleDisplacements = np.linspace(-self.alignStep[2], self.alignStep[2], 10)

        minValue = 100
        correctedPostion = [0,0,0]
        for xDis in possibleXDisplacements:
            for yDis in possibleYDisplacements:
                for angleDis in possibleAngleDisplacements:
                    self.predictedResidual =  yDis - dxdyTrack*xDis + hitY*dxdyTrack*angleDis
                    stdDev = np.mean(np.power(self.predictedResidual - self.residualY,2))
                    self.fitness.append(stdDev)
                    if minValue > stdDev:
                        minValue = stdDev
                        correctedPostion = [xDis, yDis, angleDis]
                    if abs(stdDev) < self.accuracy: 
                        self.DONE = True
                        break
                    #print xDis, yDis, angleDis,stdDev  

        newX, newY, newAngle = correctedPostion[0], correctedPostion[1], correctedPostion[2] 

        self.designAngle = self.designAngle + newAngle
        self.designX = self.designX + newX
        self.designY = self.designY + newY
        self.designEndpoints = [[ self.designX-self.length/2*math.cos( self.designAngle), self.designX+self.length/2*math.cos( self.designAngle)],[self.designY-self.length/2*math.sin( self.designAngle),self.designY+self.length/2*math.sin( self.designAngle)]]

        #print("change in X: ", newX, "step size in X: ", self.stepSizes[self.countX])
        if abs(newX) < self.stepSizes[self.countX]/2:
            self.countX += 1
        if abs(newY) < self.stepSizes[self.countY]/2:
            self.countY += 1
        if abs(newAngle) < self.stepSizes[self.countZ]/2:
            self.countZ += 1

        #print("design after align",  self.designX, self.designY, self.designAngle, self.designEndpoints)
        self.hit = [[],[]]
        self.hitXOverY = []

        self.track = [[],[]]
        self.trackXOverY = []
    def returnResidual(self):
        return self.residualY
    def isDone(self):
        return self.DONE
    def returnTime(self):
        return self.time
    def returnDesignEndpoints(self):
        return self.designEndpoints
    def returnActualEndpoints(self):
        return self.actualEndpoints
