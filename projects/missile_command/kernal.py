#!/usr/bin/python3.9

# https://stackoverflow.com/questions/15886455/simple-graphics-for-python
from graphics import GraphWin, Rectangle, Point, Circle, Line, Text
from playsound import playsound
import time, math, sys

from c6502 import Byte, Word, DWord, WordDecimal

# try for about 60 FPS
FRAMES_PER_SECOND=60
SECONDS_PER_TICK=1.0 / FRAMES_PER_SECOND
TICKS_PER_SECOND=int(1.0/SECONDS_PER_TICK)

class Frame:
    def __init__(self, action, num=0, duration=0.1):
        self.action   = action
        self.num      = Word(num)
        self.duration = Word(int(duration * TICKS_PER_SECOND))

class Animation:

    def __init__(self, item):
        self.item    = item
        self.frame_n = Byte(0)
        self.sleep   = Byte(0)

    def get_frame(self):
        return None

    def next_frame(self):
        pass

    def run_action(self, frame):
        if frame.action:
            frame.action(self,frame)


    def tick(self):

        frame = self.get_frame()
        if frame:
            if self.sleep == 0:
                self.run_action(frame)
                self.next_frame()
                if frame.duration == 0:  #no duration goto next frame
                    self.tick()
                else:
                    self.sleep = frame.duration - 1
            else:
                self.sleep = self.sleep - 1


class Graphic:

    def __init__(self):
        # graphical object
        self.graphic = []
        self.animation = None

    def undraw(self):
        for g in self.graphic:
            g.undraw()
        self.graphic = []

    def draw_to(self, win):

        self.undraw()
        self.render()
        for g in self.graphic:
            g.draw(win.win)


    def add_line(self, x1,y1,x2,y2):
        self.graphic.append(Line(Point(x1.get(), y1.get()),
                                 Point(x2.get(), y2.get())))

    def add_circle(self, x,y,radius):
        self.graphic.append(Circle(Point(x.get(), y.get()), radius.get()))

    def add_rectangle(self, x1,y1,x2,y2):
        self.graphic.append(Rectangle(Point(x1.get(), y1.get()),
                                      Point(x2.get(), y2.get())))

    def add_text(self, x,y,text):
        self.graphic.append(Text(Point(x.get(), y.get()), text))

    def render(self):
        pass


class Window:
    def __init__(self):
        self.win = GraphWin(width = 960, height = 600, autoflush = False) # create a window
        self.win.setCoords(0, 200, 320, 0) # set the coordinates of the window (mimic VGA)

    def checkMouse(self):
        return self.win.checkMouse()

    def checkKey(self):
        return self.win.checkKey()

    def redraw(self):
        self.win.redraw()
    def flush(self):
        self.win.flush()

    def wait_for_key(self):
        self.win.getKey()


class Ball(Graphic):
    def render(self):
        self.draw_circle(Byte(100),Byte(100),Byte(10))

def main():
    window = Window()
    ball = Ball()
    ball.draw_to(window)
    window.wait_for_key()


if __name__=="__main__":
    main()
