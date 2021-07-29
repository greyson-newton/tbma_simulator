from numba import jit
from geometry import scatteringDistance, scatteringAngle
from constants import *
from iterateMuon import iterateMuon
from circleIntersectLine import circleIntersectLine
import math

zBound = [-5, 5]
xDistance = 100
yBound = [-1000, 1000]

#@jit
def propagateMuon(angleInitial, speed, charge, zInitial, yInitial):
    angleInitial, speed, charge, zInitial, yInitial = angleInitial+.0, speed+.0, charge+.0, zInitial+.0, yInitial+.0
    
    #make ideal track
    try:
        slopeInital = math.tan(angleInitial)
    except:
        print("bad angle")
        return []

    final_track_pt = []

    final_track_pt[0], final_track_pt[1], final_track_pt[2] = xBound[1], xBound[1]*slopeInital + yInitial
    muonTrack = [[zInitial,zTrackFinal],[yInitial,yTrackFinal]]

    #simulate multiple scattering
    
    return muonTrack, [x_pts, y_pts,z_pts]