#!/usr/bin/python3.9


#
# purpose of this is to provide s simple graphic api that mimics
# the limitations of VERA in the X16 Commander
#
# The API isn't exactly the same as KERNAL but it close enough
# for design work
#

from c6502 import Byte, Word
from clock import Clock



class Frame:
    def __init__(self, action, num=0, duration=0.1):
        self.action   = action
        self.num      = Word(num)
        self.duration = Word(int(duration * Clock.TICKS_PER_SECOND))

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


