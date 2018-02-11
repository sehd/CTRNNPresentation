import numpy as np
from DoublePole import *
from threading import Thread

class Rnn(Thread):
    Wxh = None
    Whh = None
    Why = None
    bh = None
    by = None
    hidden_size = None
    device = None

    stopped = None

    def __init__(self,hidden_size:int, group=None, target=None, name=None, args=(), kwargs=None, daemon=None):
        self.Wxh = np.random.randn(4,hidden_size)
        self.Whh = np.random.randn(hidden_size,hidden_size)
        self.Why = np.random.randn(hidden_size,1)
        self.bh = np.zeros(hidden_size)
        self.by = np.zeros(1)
        self.hidden_size = hidden_size
        self.device = DoublePole()
        return super().__init__(group, target, name, args, kwargs)

    def SetWeightsManually(self,Wxh,Whh,Why,bh,by):
        self.Wxh = Wxh
        self.Whh = Whh
        self.Why = Why
        self.bh = bh
        self.by = by

    def run(self):
        self.device.Reset((10,5))
        self.device.start()
        self.stopped = False
        hs = np.zeros(self.hidden_size)
        while ~self.stopped:
            input = np.zeros(4)
            input[0] = self.device.degrees[0]
            input[1] = self.device.degrees[1]
            input[2] = self.device.angVelocity[0]
            input[3] = self.device.angVelocity[1]
            hs = np.tanh(np.dot(input,self.Wxh) + np.dot(self.Whh, hs) + self.bh)
            output = np.dot(hs,self.Why) + self.by
            self.device.motorState = output
        self.device.Stop()

    def Stop(self):
        self.stopped = True

    def GetState(self):
        return (self.device.degrees,self.device.angVelocity)