#!/usr/bin/python3.9

import time

from c6502 import Word
from list import Item, List

class Alarm(Item):

    def __init__(self):
        super().__init__()

    def set(self, clock, alarm_ticks, callback, param):
        self.clock = clock
        self.alarm_ticks = alarm_ticks
        self.callback = callback
        self.param = param

    def check(self):
        if self.active == True:
            if self.alarm_ticks < self.clock.ticks:
                if self.param is None:
                    self.callback()
                else:
                    self.callback(self.param)
                self.destroy()

class Clock:

    # try for about 60 FPS
    FRAMES_PER_SECOND=30
    SECONDS_PER_TICK=1.0 / FRAMES_PER_SECOND
    TICKS_PER_SECOND=int(1.0/SECONDS_PER_TICK)

    def __init__(self):
        self.ticks = Word(0)
        self.alarm = List(Alarm, 10)


        self.loop_start  = time.time()
        self.extra_sleep = 0


        self.frame_cnt    = 0
        self.frame_start = time.time()
        self.fps         = Clock.FRAMES_PER_SECOND


    # https://stackoverflow.com/questions/1133857/how-accurate-is-pythons-time-sleep/
    def sleep(duration, get_now=time.perf_counter):
        now = get_now()
        time.sleep(duration/1.1)
        end = now + duration
        while now < end:
            now = get_now()

    def tick(self):
        self.ticks.set(self.ticks.get()+1)

        self.frame_cnt = self.frame_cnt + 1
        actual_total_seconds = time.time() - self.frame_start
        expected_total_seconds = self.frame_cnt * Clock.SECONDS_PER_TICK
        sleep_seconds = expected_total_seconds - actual_total_seconds

        if sleep_seconds > 0:
            Clock.sleep(sleep_seconds)

        #
        # update fps stats
        #
        if self.frame_cnt % 10 == 0:
            now = time.time()
            self.fps = self.frame_cnt / (now - self.frame_start)


    def reset(self):
        self.ticks.set(0)
        self.alarm.clear()

    def set_alarm(self, wait_seconds, callback, param=None):
        alarm = self.alarm.create()

        sleep_until = self.ticks + int(wait_seconds * Clock.TICKS_PER_SECOND)
        alarm.set(self, sleep_until, callback, param)

    def check_alarms(self):
        for alarm in self.alarm.items:
            alarm.check()





def print_func(msg):
    print(msg)

def main():

    clock = Clock()

    clock.set_alarm(4, print_func, "Hello")
    clock.set_alarm(6, print_func, "World")
    clock.set_alarm(10, print_func, "How")
    clock.set_alarm(20, print_func, "Are")
    clock.set_alarm(21, print_func, "You!!!!!!!!")

    while True:
        clock.tick()
        clock.check_alarms()


if __name__=="__main__":
    main()

