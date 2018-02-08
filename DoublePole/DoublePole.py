from math import *
from datetime import *
from threading import Thread
from time import sleep
class DoublePole(Thread):
    lengths = (1,1)
    degrees = (pi,pi)
    angVelocity = (0,0)
    rou = (0.1,0.1)
    Stopped = True
    previousTime = None
    g = 9.81 #Gravitational Constant

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, daemon=None):
        return super().__init__(group,target,name,args,kwargs)

    def Reset(self,lengths:tuple):
        self.lengths = lengths
        self.degrees = (pi / 4,0)
        self.angVelocity = (0,0)
        self.Stopped = True
    
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
            torque = self.getTorque(self.rou,self.lengths,self.degrees,self.g)
            I = (self.rou[0] * self.lengths[0] / 3,self.rou[1] * self.lengths[1] / 3)
            self.angVelocity = self.calculateW((torque[0] / I[0],
                 torque[1] / I[1]),
                 self.angVelocity,deltaT)
            self.degrees = (self.degrees[0] + self.angVelocity[0] * deltaT,self.degrees[1] + self.angVelocity[1] * deltaT)
            sleep(0.05)

    def getTorque(self,rou:tuple,length:tuple,theta:tuple,g:float):
        t1 = -rou[0] * (length[0] ^ 2) * g * cos(theta[0]) / 2 + rou[1] * (length[1] ^ 2) * g * sin(theta[1]) * sin(theta[0] - theta[1])
        t2 = -rou[1] * (length[1] ^ 2) * g * cos(theta[1]) / 2
        return (t1,t2)

    def calculateW(self,alpha:tuple,currentW:tuple,deltaT:float):
        w1 = alpha[0] * deltaT + currentW[0]
        w2 = alpha[1] * deltaT + currentW[1]
        return (w1,w2)
