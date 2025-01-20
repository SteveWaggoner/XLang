#!/usr/bin/python3.9

import math

# https://stackoverflow.com/questions/15886455/simple-graphics-for-python
from graphics import Rectangle, Point, Circle, Line, Text, Image
from c6502 import Byte, Word, WordDecimal

from list import Item, List
from clock import Clock


# really a vector in the case of velocity
class Position:

    def __init__(self,x,y):
        self.x = WordDecimal().set(x)
        self.y = WordDecimal().set(y)
    def __str__(self):
        return str(round(self.x.get(),2))+","+str(round(self.y.get(),2))


    def distance_to(self, other):
        # manhattan distance
        return (self.x - other.x).abs() + (self.y - other.y).abs()
        # chebyshev distance
      #  return max((self.x - other.x).abs(), (self.y - other.y).abs())

        # true distance
      #  return math.sqrt(((self.x.get() - other.x.get()) * (self.x.get() - other.x.get())) + \
      #                   ((self.y.get() - other.y.get()) * (self.y.get() - other.y.get())))


    def calculate_velocity_to(self, dest, speed):

        delta_x = (dest.x - self.x)
        delta_y = (dest.y - self.y)

        rough_distance_in_pixels = self.distance_to(dest)
        pixels_per_tick = speed
        ticks_until_dest = rough_distance_in_pixels / pixels_per_tick

        delta_x_per_tick = (delta_x / ticks_until_dest)
        delta_y_per_tick = (delta_y / ticks_until_dest)

        velocity = Position(delta_x_per_tick.get(),delta_y_per_tick.get())
        return velocity


class Object(Item):

    def __init__(self):
        super().__init__()

        # memory allocation
        self.active = Byte(False)

        #location and size
        self.start    = None   # origin of missile/bomb
        self.pos      = None
        self.dest     = None
        self.velocity = None
        self.distance = None
        self.last_distance = None

        self.width  = Word()
        self.height = Word()
        self.radius = Word(1)   # all enemys have a radius so just default

        self.route = None
        self.route_n = Byte(0)
        self.last_dodge = Word(0)
        self.destroy_at_dest = Byte(False)

        # graphical object
        self.graphic = []
        self.animation = None

    def __str__(self):
        return self.__class__.__name__ + "(pos="+str(self.pos)+", w="+str(self.width)+", h="+str(self.height)+", r="+str(self.radius) \
            +", dest="+str(self.dest)+", velocity="+str(self.velocity)+", dist="+str(self.distance)+")"


    def collide_circles(self, other):
        diff_x = (self.pos.x - other.pos.x).abs()
        if diff_x < self.radius + other.radius:
            diff_y = (self.pos.y - other.pos.y).abs()
            if diff_y < self.radius + other.radius:
                return True
        return False

    def collide_pnt_in_rect(self, other):
        if self.pos.x > other.pos.x and self.pos.x < other.pos.x + other.width:
            if self.pos.y > other.pos.y and self.pos.y < other.pos.y + other.height:
                return True
        return False

    def set_position(self, start, dest=None, speed=None, width=None, height=None):

        self.start = start
        self.pos   = Position(start.x,start.y)

        if not width is None:
            self.width.set(width)
            self.height.set(height)

        if dest:
            self.dest  = dest
            self.speed = (speed / Clock.TICKS_PER_SECOND)  #speed is converted from pixels_per_second to pixels_per_tick
            self.update_vectors()


    def update_vectors(self):
        self.velocity = self.pos.calculate_velocity_to(self.dest, self.speed)
        print(f"self.pos = {self.pos}, self.dest = {self.dest}, self.speed={self.speed}, self.velocity = {self.velocity}")


    def move(self):
        self.pos.x = self.pos.x + self.velocity.x
        self.pos.y = self.pos.y + self.velocity.y
        self.last_distance = self.distance
        self.distance = self.pos.distance_to(self.dest)


    def destroy(self):
        super().destroy()
        self.undraw()

    def render(self,win):
        # dummy
        self.add_circle(self.start.x, self.start.y, Byte(3))


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
        self.graphic.append(bitmap.get_image())





def main():
    objects = List(Object,5)
    huh = objects.create()
    print(huh)


    start_pos = Position(50,0)
    end_pos   = Position(0,50)

    vel = start_pos.calculate_velocity_to(end_pos, 1)
    print(f"start={start_pos}, end={end_pos}, vel={vel}")

    vel2 = start_pos.calculate_velocity_to(end_pos, 2)
    print(f"start={start_pos}, end={end_pos}, vel={vel2}")

    vel3 = start_pos.calculate_velocity_to(end_pos, 3)
    print(f"start={start_pos}, end={end_pos}, vel={vel3}")



if __name__=="__main__":
    main()

