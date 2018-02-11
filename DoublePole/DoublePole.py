from math import *
from datetime import *
from threading import Thread
from time import sleep

class DoublePole(Thread):
    
    #System State
    lengths = None
    degrees = None
    angVelocity = None
    motorState = None

    #Pre-calculated values
    negativeHalfOfRouL2g = None
    rouL2g = None
    angularMomentOfInertia = None

    #Temporary hold
    Stopped = True
    previousTime = None

    #Constants
    g = 9.81
    rou = (0.1,0.1)
    maxTorque = 200

    def Reset(self,lengths:tuple):
        self.lengths = lengths
        self.degrees = (pi / 2,pi / 2 - 0.1)
        self.angVelocity = (0,0)
        self.motorState = 0
        self.Stopped = True
        self.negativeHalfOfRouL2g = (-self.rou[0] * self.lengths[0] ** 2 * self.g / 2,-self.rou[1] * self.lengths[1] ** 2 * self.g / 2)
        self.rouL2g = (None,self.rou[1] * self.lengths[1] ** 2 * self.g)
        self.angularMomentOfInertia = (self.rou[0] * self.lengths[0] / 3,self.rou[1] * self.lengths[1] / 3)
    
    def run(self):
        self.previousTime = datetime.now()
        self.Stopped = False
        self.Loop()

    def Stop(self):
        Stopped = True

    def Loop(self):
        while ~self.Stopped:
            currentTime = datetime.now()
            deltaT = (currentTime - self.previousTime).total_seconds() / 10
            self.previousTime = currentTime
            torque = self.getTorque()
            torque[0]+=self.maxTorque * self.motorState
            self.angVelocity = self.calculateW((torque[0] / self.angularMomentOfInertia[0],
                 torque[1] / self.angularMomentOfInertia[1]),deltaT)
            self.degrees = (self.degrees[0] + self.angVelocity[0] * deltaT,self.degrees[1] + self.angVelocity[1] * deltaT)
            #sleep(0.05)

    def getTorque(self):
        t1 = self.negativeHalfOfRouL2g[0] * cos(self.degrees[0]) + self.rouL2g[1] * sin(self.degrees[1]) * sin(self.degrees[0] - self.degrees[1])
        t2 = self.negativeHalfOfRouL2g[1] * cos(self.degrees[1]) 
        return [t1,t2]

    def calculateW(self,alpha:tuple,deltaT:float):
        w1 = alpha[0] * deltaT + self.angVelocity[0]
        w2 = alpha[1] * deltaT + self.angVelocity[1]
        return (w1,w2)
