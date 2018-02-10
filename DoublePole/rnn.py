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
    device = DoublePole()

    stopped = None

    def __init__(self,hidden_size:int, group=None, target=None, name=None, args=(), kwargs=None, daemon=None):
        self.Wxh = np.random.randn(4,hidden_size)
        self.Whh = np.random.randn(hidden_size,hidden_size)
        self.Why = np.random.randn(hidden_size,3)
        self.bh = np.zeros(hidden_size)
        self.by = np.zeros(3)
        self.hidden_size = hidden_size
        return super().__init__(group, target, name, args, kwargs)

    def SetWeightsManually(self,Wxh,Whh,Why):
        self.Wxh = Wxh
        self.Whh = Whh
        self.Why = Why

    def run(self):
        self.device.Reset((10,5))
        self.device.start()
        self.stopped = False
        hs = np.zeros(hidden_size)
        while ~self.stopped:
            input = np.zeros(4)
            input[0] = self.device.degrees[0]
            input[1] = self.device.degrees[1]
            input[2] = self.device.angVelocity[0]
            input[3] = self.device.angVelocity[1]
            self.hs = np.tanh(np.dot(self.Wxh, input) + np.dot(self.Whh, self.hs) + bh)
            output = np.dot(self.Why,self.hs) + by
            mx = max(output)
            if(output[0] == mx):
                self.device.motorState = (True,False)
            elif(output[1] == mx):
                self.device.motorState = (False,False)
            else:
                self.device.motorState = (True,True)
        self.device.Stop()

    def Stop(self):
        self.stopped = True

    def GetState(self):
        return (self.device.degrees,self.device.angVelocity)