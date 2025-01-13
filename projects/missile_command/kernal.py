#!/usr/bin/python3.9


#
# purpose of this is to provide s simple graphic api that mimics
# the limitations of VERA in the X16 Commander
#
# The API isn't exactly the same as KERNAL but it close enough
# for design work
#



# https://stackoverflow.com/questions/15886455/simple-graphics-for-python
from graphics import GraphWin, Rectangle, Point, Circle, Line, Text, Image
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
        self.render(win)
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

    def add_image(self, image):
        self.graphic.append(image)

    def add_bitmap(self, bitmap):
        self.graphic.append(bitmap.resized_image())

    def render(self,win):
        pass




class Bitmap:

    # todo: make this not use tkinter
    def get_image_size(path):
        from graphics import _root
        try:  # import as appropriate for 2.x vs. 3.x
           import tkinter as tk
        except:
           import Tkinter as tk

        img = tk.PhotoImage(file=path, master=_root)
        return (img.width(),img.height())


    def __init__(self,x=None,y=None,path=None,width=None,height=None,scale_x=1,scale_y=1,scale_to_win=None):

        # figure out width,height from path (if necessary)
        if width is None:
            width, height = Bitmap.get_image_size(path)

        # figure out anchor from width,height (if necessary)
        if x is None:
            x = width / 2
            y = height / 2

        # if path is None... then blank image
        if path is None:
        	self.image = Image(Point(x,y), width, height)
        else:
        	self.image = Image(Point(x,y), path)

        self.scale_to_win = scale_to_win
        self.scale_x = scale_x
        self.scale_y = scale_y

    def resized_image(self):
        resized_image = self.image.clone()

        if self.scale_to_win is not None:
            resized_image.img = resized_image.img.zoom(self.scale_to_win.background_bitmap.scale_x,
                                                       self.scale_to_win.background_bitmap.scale_y)
        else:
            resized_image.img = resized_image.img.zoom(self.scale_x,self.scale_y)
        return resized_image

    #bitmap api
    def get_width(self):
        return self.image.getWidth()

    def get_height(self):
        return self.image.getHeight()

    def get_pixel(self, x,y):
        return self.image.getPixel(x,y)

    def put_pixel(self, x,y,color):
        self.image.setPixel(x,y,color)

    def fill_rect(self, x,y,width,height,color):
        for i in range(width):
            for j in range(height):
                self.put_pixel(x+i,y+j,color)


    def fill_pixels(self, x,y,numPixels,color):
        pass


    def get_pixels(self, x,y,numPixels):
        pass

    def put_pixels(self, x,y,numPixels,pixelBuffer,maskBuffer,transparentColor,rasterOperation):
        pass

    def get_block(self, x,y,width,height):
        pass

    def put_block(self, x,y,width,height,pixelBuffer,maskBuffer,transparentColor,rasterOperation):
        pass

    def draw_text(self, x,y, text):
        pass




class Window:
    def __init__(self, mode="VGA"):
        self.set_mode(mode)

    def set_mode(self,mode):

        if mode == "VGA":
            width   = 320
            height  = 200
            scale_x = 4
            scale_y = 4
        elif mode == "C64_MC":
            width   = 160
            height  = 200
            scale_x = 8
            scale_y = 4

        self.win = GraphWin(width = width*scale_x, height = height*scale_y, autoflush = False) # scaled-up a window
        self.win.setCoords(0, height, width, 0)  #invert the y coordinate
        self.background_bitmap = Bitmap(width=width,height=height,scale_x=scale_x,scale_y=scale_y)
        self.last_bkgnd_image = None

    def update_background(self):

        if not self.last_bkgnd_image is None:
            self.last_bkgnd_image.undraw()
        self.last_bkgnd_image = self.background_bitmap.resized_image()
        self.last_bkgnd_image.draw(self.win)


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
    def render(self,win):
        self.add_circle(Byte(100),Byte(100),Byte(10))

class BeachBall(Graphic):
    def render(self,win):
        self.bitmap = Bitmap(150,150,"images/bouncing_beach_ball.png", scale_to_win=win)
        self.add_bitmap(self.bitmap)

class Lemmings(Graphic):
    def render(self,win):
        self.add_bitmap(Bitmap(path="images/Lemmings.png",scale_to_win=win))

class C64_Art(Graphic):
    def render(self,win):
        self.bitmap = Bitmap(path="images/C64_Art.png",scale_to_win=win)
        self.add_bitmap(self.bitmap)



def main():

    window = Window("VGA")

    bkgnd = window.background_bitmap

    bkgnd.put_pixel(0,0,"black")
    bkgnd.put_pixel(0,1,"black")
    bkgnd.put_pixel(1,0,"black")
    bkgnd.put_pixel(1,1,"black")
    bkgnd.put_pixel(2,0,"black")
    bkgnd.put_pixel(2,1,"black")

    bkgnd.fill_rect(50,50,32,32,"blue")
#    bkgnd.fill_rect(150,150, 5,5,"green")
#    bkgnd.fill_rect(290,190, 5,5,"yellow")

    window.update_background()


#    c64_art = C64_Art()
#    c64_art.draw_to(window)

    lemmings = Lemmings()
    lemmings.draw_to(window)

    ball = Ball()
    ball.draw_to(window)


    beach_ball = BeachBall()
    beach_ball.draw_to(window)



    window.wait_for_key()


if __name__=="__main__":
    main()
