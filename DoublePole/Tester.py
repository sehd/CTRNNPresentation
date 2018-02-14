from DoublePole import DoublePole
from time import sleep
from graphics import *
from math import *

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

dp = DoublePole()
dp.Reset((10,5))
dp.start()
win = GraphWin('Double Pole Viewer',800,600)
lines = CalculateLines((dp.lengths[0] * 10,dp.lengths[1] * 10),dp.degrees)
for x in range(1,10000):
    lines[0].undraw()
    lines[1].undraw()
    lines = CalculateLines((dp.lengths[0] * 10,dp.lengths[1] * 10),dp.degrees)
    lines[0].draw(win)
    lines[1].draw(win)
    sleep(0.01)
    key = win.checkKey()
    if(key == 'Left'):
        dp.motorState =1
    elif(key == 'Right'):
        dp.motorState =-1
    else:
        dp.motorState = 0

dp.Stop()
win.close()
