from DoublePole import DoublePole
from time import sleep
from graphics import *
from math import *
from threading import Thread

class DoublePoleVisualizer(object):
    lines = None
    win = None
    dp = None
    
    def CalculateLines(self,lengths:tuple,theta:tuple):
        if((lengths is None) or (theta is None)):
            return None
        origin = Point(400,300)
        eop1 = Point(lengths[0] * cos(theta[0]) + origin.x,-lengths[0] * sin(theta[0]) + origin.y)
        eop2 = Point(lengths[1] * cos(theta[1]) + eop1.x,-lengths[1] * sin(theta[1]) + eop1.y)
        p1 = Line(origin,eop1)
        p1.setWidth(5)
        p1.setFill('red')
        p2 = Line(eop1,eop2)
        p2.setWidth(5)
        p2.setFill('blue')
        return (p1,p2)

    def run(self):
        self.Loop()

    def SetPoles(self,doublePole:DoublePole):
        self.dp = doublePole
        self.win = GraphWin('Double Pole Viewer',800,600)
        self.lines = self.CalculateLines(self.dp.lengths,self.dp.degrees)
    
    def Loop(self):
        while True:
            if(self.lines is None):
                sleep(0.1)
                self.lines = self.CalculateLines(self.dp.lengths,self.dp.degrees)
                continue
            self.lines[0].undraw()
            self.lines[1].undraw()
            self.lines = self.CalculateLines(self.dp.lengths,self.dp.degrees)
            self.lines[0].draw(self.win)
            self.lines[1].draw(self.win)
            sleep(0.1)
    
        