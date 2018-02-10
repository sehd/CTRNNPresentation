from numpy import numpy as np
from DoublePole import *
from threading import Thread

class Rnn(Thread):
    Wxh = None
    Whh = None
    Why = None
    hidden_size = None
    device = DoublePole()

    def __init__(self,hidden_size:int, group=None, target=None, name=None, args=(), kwargs=None, daemon=None):
        self.Wxh = np.random.randn(4,hidden_size)
        self.Whh = np.random.randn(hidden_size,hidden_size)
        self.Why = np.random.randn(hidden_size,3)
        self.hidden_size = hidden_size
        return super().__init__(group, target, name, args, kwargs, daemon)

    def SetWeightsManually(self,Wxh,Whh,Why):
        self.Wxh = Wxh
        self.Whh = Whh
        self.Why = Why

    def run(self):
        pass

    def Stop(self):
        pass

    def GetState(self):
        pass