#!/usr/bin/python3.9

import time, math, sys

from c6502 import Byte, WordDecimal

from kernal import TICKS_PER_SECOND


# really a vector in the case of velocity
class Position:

    def __init__(self,x,y):
        self.x = WordDecimal().set(x)
        self.y = WordDecimal().set(y)
    def __str__(self):
        return str(round(self.x.get(),2))+","+str(round(self.y.get(),2))


    def distance_to(self, other):
        # manhattan distance
      #  return (self.x - other.x).abs() + (self.y - other.y).abs()
        # chebyshev distance
        return max((self.x - other.x).abs(), (self.y - other.y).abs())


    def calculate_velocity_to(self, dest, speed):

        delta_x = (dest.x - self.x)
        delta_y = (dest.y - self.y)

        rough_distance_in_pixels = delta_x.abs() + delta_y.abs()
        pixels_per_second = speed
        seconds_until_dest = rough_distance_in_pixels / pixels_per_second

        print(" seconds_until_dest = "+str(seconds_until_dest))
        print(" TICKS_PER_SECOND   = "+str(TICKS_PER_SECOND))

        #
        # the " / 2" is to prevent the number getting too big for WordDecimal when FPS>60
        #

        ticks_until_dest = seconds_until_dest * int( TICKS_PER_SECOND / 2)

        print(" ticks_until_dest   = "+str(ticks_until_dest))

        delta_x_per_tick = (delta_x / ticks_until_dest) / 2
        delta_y_per_tick = (delta_y / ticks_until_dest) / 2

        velocity = Position(delta_x_per_tick.get(),delta_y_per_tick.get())
        return velocity


#
# fixed memory dynamic array (c) 2025 wagtech baby
#

class ItemList:

    def __init__(self, item_class, max_items, active=0):

        self.num_active = Byte(0)
        self.next_alloc = Byte(0)
        self.items = []
        for x in range(max_items):
            i = item_class()

            print(i)

            i.list = self
            i.active = active
            self.items.append(i)

    def __getitem__(self, key):
        return self.items[key]

    def create(self):

        n = self.next_alloc.get()
        i = 0

        while i < len(self.items):
            if self.items[n].active == False:
                self.items[n].active = True
                self.next_alloc.set( ( n + 1 ) % len(self.items) )
                self.num_active.set( self.num_active + 1 )
                print("created "+str(self.items[n].__class__.__name__)+" "+str(n))
                return self.items[n]
            i = i + 1
            n = (n + 1) % len(self.items)

        print("bad alloc")
        die = 0/0
        return None

    def clear(self):
        for i in self.items:
            i.destroy()


    def get_collisions(self, other, has_collided_function):
        hits = []
        for a in self.items:
            if a.active:
                for b in other.items:
                    if b.active:
                        if has_collided_function(a,b):
                            hits.append((a,b))
        return hits


