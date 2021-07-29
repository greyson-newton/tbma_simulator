Run the graphicsRemote file to execute program.

To run multiple simulations on the same window, after first simulation has completed click 
the RESET Btn, change whatever parameters needed for the new simulation, then click the START Btn 
to begin next simulation. 

Each simulation adds an entry to a text file named "Log" detailing the parameters and the time it took 
to complete. To view the log, click the LOG Btn.

Future Changes: add different alignment algorithms and test the efficiency of each algorithm.


Environment setup for a track-based muon alignment(tbma)

An example first, setting up a simulation for a movie theatre visit, you have to arrive and buy a ticket first.
Upon inspection, cashiers are a **resource** that the theater makes available to its customers, 
and they help moviegoers through the **process** of purchasing a ticket.


UPDATES [07/227-29]

[1] - simulation manager - simpy
    Modulates and manages processes, resources and methods
------------------------------------------------------------------------------------------------------------
    ARRIVE AT MOVEIS
    Position the initial actual and design chamber positions(arriving at movies)
    returns chamber data

    GET TO YOUR SEAT

    [i] 
        Generate Muon Data  : propagateMuon.py
            Resources   - chamber position (2x 3d Rectangles)
            Method      -  Monte Carlo Muon propagation
                Resources   - chamber data to construct cone of muon gun around
                Methods     - propagateMuon.py -> shootMuons()

        RETURNS muonTrack through 2x 3d points (straight line w/ no scattering) and
        muonPath through many 3d points (piecewise 3d line ) 
                    
    [ii] 
        Find Hits : chamber.py->get_hits()
            Dependencies    - geometry.py
            Resources       - muon-track, and chamber data 
            Process 
                [1] FIND predicted hit i.e. "track"
                    Dependencies    - geometry.py->intersectAndHit()
                                    geometry.py->returnLocalDxDy()
                                    geometry.py->transformCord()
                    Resources       - design chamber width, height, center position 
                                    - muonTrack 
                    Example
                                    [a] intersectAndHit(self.designEndpoints, muonTrack)
                                    [b] trackSlope = returnLocalDxDy(self.designAngle, muonTrack)
                                    [c] transformedInterceptTrack = transformCord(self.designX, self.designY, self.designAngle, interceptTrack)
                RETURNS muonTrack "HIT" data
                [1a] - did it hit design chamber?     

                [2] FIND actual hit i.e. "path"
                    Dependencies    - [1]
                    Resources       - actual chamber width, height, center position
                                    - muonTrack
                RETURNS muonPath "HIT" data
                [2a] - did path actual chamber?

    From HIT data, if [1a] and [2a] true then continue to

    [iii] 
        Align chamber () chamber.py -> align()
        Resources - chamber, muonTrack/Path, HIT and grad_desc parameters,  
        Dependencies - geometry.py
                    - momentum.py 
        Process
            [1] Calculate Residual
                    - self.residualY = trackY-hitY
            [2] Shift actual chamber in X,Y,Z,eta,theta,phi by stepsize
                    - Magnitude of Stepsize Depends on momentum.py   
                [2a] Calculate Residual stdDev between actual and predicted residual for each combination of shifts
                        - self.predictedResidual =  yDis - dxdyTrack*xDis + hitY*dxdyTrack*angleDis
                        - stdDev = np.mean(np.power(self.predictedResidual - self.residualY,2))
                [2b] If stdDev is less than the previous lowest -> apply stepsize shifts to actual chamber
                    - Increment stepsize in directions of applied shifts
            [3] Every shootMuons() updates the plot
            [4] Repeat [1] & [2] until 
                    - abs(stdDev) < self.accuracy


    [i]
    propagateMuon()
        init_angle, init_speed = 1, 1000
        init_x,init_y,init_z = 0,0,0
        muonPath, muonTrack = []
    RETURNS muonTrack, ScatteringPoints [x,y,z] of muonPath
    [ii]

    ------------------------------------------------------------------------------------------------------------
[2] DataManager
    better name for it would be simulation_manager 

    -Implemented a 3d geometry system
    -consolidated these classes into DataManager
        *multipleScattering 
        *chamber is now a list of vectors(3d)
        *created a "Muon" class - extends vec3 class
        *propogate, shoot muons
        
    -Stopped at consolidating alignment algorithm