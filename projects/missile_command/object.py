#!/usr/bin/python3.9

import math

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


class Action:
    def __init__(self, callback, num=0, duration=0.1):
        self.callback = callback
        self.param    = Word(num)
        self.duration = Word(int(duration * Clock.TICKS_PER_SECOND))

    def run(self, obj):
        self.callback(obj, self)

    #example callbacks actions
    def set_radius(obj, action):
        obj.radius = action.param
    def destroy(obj, action):
        obj.destroy()



class Object(Item):

    def __init__(self):
        super().__init__()

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
        self.route_index = Byte(0)
        self.last_dodge = Word(0)
        self.destroy_at_dest = Byte(False)

        # behavior
        self.actions = None
        self.action_index = Byte(0)
        self.action_sleep = Byte(0)

        self.move_cnt = 0

    def __str__(self):
        return self.__class__.__name__ + "(start="+str(self.start)+", mc="+str(self.move_cnt) \
            +", ai/as="+str(self.action_index)+"/"+str(self.action_sleep)+", pos="+str(self.pos) \
            +", w="+str(self.width)+", h="+str(self.height)+", r="+str(self.radius) \
            +", dest="+str(self.dest)+", velocity="+str(self.velocity)+", dist="+str(self.distance)+")"


    def get_hash(self, prev_hash=""):
        return prev_hash+"|"+str(self)

    #
    # for object collision detection
    #
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

    #
    # for object motion
    #
    def set_position(self, start, dest=None, speed=None, width=None, height=None):

        self.start = start
        self.pos   = Position(start.x,start.y)

        self.move_cnt = 0 #debug

        if not width is None:
            self.width.set(width)
            self.height.set(height)

        if dest:
            self.dest  = dest
            self.speed = (speed / Clock.TICKS_PER_SECOND)  #speed is converted from pixels_per_second to pixels_per_tick
            self.update_vectors()

    def update_vectors(self):
        self.velocity = self.pos.calculate_velocity_to(self.dest, self.speed)

    def move(self):
        self.move_cnt = self.move_cnt + 1
        self.pos.x = self.pos.x + self.velocity.x
        self.pos.y = self.pos.y + self.velocity.y
        self.last_distance = self.distance
        self.distance = self.pos.distance_to(self.dest)

    #
    # for object targeting
    #
    def get_target_pos(self):
        #get center mass of object ("pos" is anchor top upper corner for rectangles so more to center bottom)
        if self.width > 0:
            return Position(self.pos.x + (self.width/2), self.pos.y + self.height)
        else:
            return self.pos

    #
    # for object behavior (e.g. explosion morphing, etc.)
    #
    def next_action(self):
        self.action_index = ( self.action_index + 1 ) % len(self.actions)

    def action_tick(self):

        if self.actions is not None:

            action = self.actions[self.action_index.get()]
            if self.action_sleep > 0:
                self.action_sleep -= 1
            else:
                action.run(self)
                self.action_sleep = action.duration
                self.next_action()
                if self.action_sleep == 0:
                    self.action_tick()  # immediately run next action if zero duration






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

