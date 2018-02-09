from DoublePole import DoublePole
from time import sleep
from graphics import *
from math import *
from threading import Thread

class DoublePoleVisualizer(Thread):
    lines = None
    win = None

    def run(self):
        Loop()

    def SetPoles(self,doublePole:DoublePole):
        self.win = GraphWin('Double Pole Viewer',800,600)
        self.lines = CalculateLines(dp.lengths,dp.degrees)

    def CalculateLines(lengths:tuple,theta:tuple):
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
    
    def Loop():
        while True:
            lines[0].undraw()
            lines[1].undraw()
            lines = CalculateLines(dp.lengths,dp.degrees)
            lines[0].draw(win)
            lines[1].draw(win)
            sleep(0.1)
    
        