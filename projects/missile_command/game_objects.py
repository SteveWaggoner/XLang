#!/usr/bin/python3.9

from c6502 import Byte, Word, WordDecimal
from object import Position, Object
from animation import Animation, Frame
from clock import Clock

class Action:
    def set_radius(animation, frame):
        animation.item.radius = frame.num
    def destroy(animation, frame):
        animation.item.destroy()


class ExplosionAnimation(Animation):

    frames = []
    frames.append(Frame(Action.set_radius, num=6))
    frames.append(Frame(Action.set_radius, num=10))
    frames.append(Frame(Action.set_radius, num=20))
    frames.append(Frame(Action.set_radius, num=18))
    frames.append(Frame(Action.set_radius, num=20))
    frames.append(Frame(Action.set_radius, num=18))
    frames.append(Frame(Action.set_radius, num=16))
    frames.append(Frame(Action.set_radius, num=14))
    frames.append(Frame(Action.set_radius, num=8))
    frames.append(Frame(Action.set_radius, num=4))
    frames.append(Frame(Action.destroy))

    def get_frame(self):
        return ExplosionAnimation.frames[self.frame_n.get()]

    def next_frame(self):
        self.frame_n = ( self.frame_n + 1 ) % len(ExplosionAnimation.frames)

class PlaneAnimation(Animation):

    frames = []
    frames.append(Frame(Action.set_radius, num=5, duration=3))
    frames.append(Frame(Action.set_radius, num=6, duration=5))
    frames.append(Frame(Action.set_radius, num=5, duration=1))
    frames.append(Frame(Action.set_radius, num=4, duration=1))

    def get_frame(self):
        return PlaneAnimation.frames[self.frame_n.get()]

    def next_frame(self):
        self.frame_n = ( self.frame_n + 1 ) % len(PlaneAnimation.frames)





class Object_Missile(Object):
    def __init__(self):
        super().__init__()
        self.destroy_at_dest.set(True)

    def render(self,win):
        self.add_line(self.start.x, self.start.y, self.pos.x, self.pos.y)
        self.add_circle(self.pos.x, self.pos.y, Byte(1))

class Object_Bomb(Object):
    def render(self,win):
        self.add_line(self.start.x, self.start.y, self.pos.x, self.pos.y)
        self.add_circle(self.pos.x, self.pos.y, Byte(1))

class Object_SmartBomb(Object):
    def render(self,win):
        self.add_line(self.pos.x-2, self.pos.y-2, self.pos.x+2, self.pos.y+2)
        self.add_line(self.pos.x+2, self.pos.y-2, self.pos.x-2, self.pos.y+2)
        self.add_circle(self.pos.x, self.pos.y, Byte(1))


class Object_Plane(Object):
    def __init__(self):
        super().__init__()
        self.animation = PlaneAnimation(self)
        self.destroy_at_dest.set(True)

    def render(self,win):
        self.add_circle(self.pos.x, self.pos.y, self.radius)

class Object_Alien(Object):
    def __init__(self):
        super().__init__()
        self.width.set(3)
        self.height.set(3)
        self.destroy_at_dest.set(1)

    def render(self,win):
        self.add_rectangle(self.pos.x, self.pos.y, self.pos.x+self.width, self.pos.y+self.height)

class Object_Mario(Object):
    def __init__(self):
        super().__init__()
        self.width.set(3)
        self.height.set(3)
       # self.destroy_at_dest.set(1)

    def render(self,win):
        self.add_rectangle(self.pos.x, self.pos.y, self.pos.x+self.width, self.pos.y+self.height)

        win.background.img.fill_rect(int(self.pos.x.get()), int(self.pos.y.get()), int(self.width.get()), int(self.height.get()), "#F0D30F")
        pass


class Object_Explosion(Object):
    def __init__(self):
        super().__init__()
        self.animation = ExplosionAnimation(self)

    def render(self,win):
        self.add_circle( self.pos.x, self.pos.y, self.radius)

class Object_Battery(Object):
    def __init__(self):
        super().__init__()
        self.num_missiles = Byte(0)

    def render(self,win):
        self.add_rectangle(self.pos.x, self.pos.y,
                           self.pos.x + self.width, self.pos.y + self.height)
        self.add_text(self.pos.x + self.width/2, self.pos.y + self.height/2, str(self.num_missiles))


class Object_City(Object):
    def __init__(self):
        super().__init__()
        self.destroyed = Byte(False)

    def render(self,win):
        if self.destroyed.get():
            self.add_rectangle(self.pos.x, self.pos.y + (self.height-1),
                               self.pos.x+self.width, self.pos.y + self.height)
        else:
            self.add_rectangle(self.pos.x, self.pos.y,
                                self.pos.x + self.width, self.pos.y + self.height)

class Object_Land(Object):
    def render(self,win):
        self.add_rectangle(self.pos.x, self.pos.y,
                           self.pos.x + self.width, self.pos.y + self.height)


class UI(Object):

    def set_fields(self, level, score, game_over, debug):
        self.level = level
        self.score = score
        self.game_over = game_over
        self.debug = debug

    def render(self,win):
        self.add_text(Byte(60), Byte(20), str(self.debug))
        self.add_text(Byte(180), Byte(10), "level: "+str(self.level)+"   score:" + str(self.score))
        if self.game_over.get():
            self.add_text(Byte(180), Byte(100), "GAME OVER")


class Enemy:

    def __init__(self, enemy, start, speed, dest=None, launch_time=None, attack_times=None, attack_types=None, route=None):
        self.enemy = enemy
        self.start = start
        self.dest = dest
        self.speed = speed

        if not launch_time is None:
            #convert from seconds to ticks (ie. we can increase frame rate and timing doesn't change for level)
            self.launch_time = int(launch_time * Clock.TICKS_PER_SECOND)
        if not attack_times is None:
            #convert from seconds to ticks (ie. we can increase frame rate and timing doesn't change for level)
            self.attack_times = [int(s * Clock.TICKS_PER_SECOND) for s in attack_times]

        self.attack_types = attack_types
        self.route = route
        if self.dest is None:
            self.dest = self.route.pop(0)

    def spawn(self, game):
        if self.enemy == "bomb":
            enemy = game.bomb.create()
        elif self.enemy == "smartbomb":
            enemy = game.smartbomb.create()
        elif self.enemy == "mario":
            enemy = game.mario.create()
        elif self.enemy == "plane":
            enemy = game.plane.create()
            enemy.attack_times = self.attack_times
            enemy.attack_types = self.attack_types
        elif self.enemy == "alien":
            enemy = game.alien.create()
            enemy.attack_times = self.attack_times
            enemy.attack_types = self.attack_types
            if self.route:
                enemy.route = self.route.copy()
        else:
            raise Exception("unknown enemy: "+self.enemy)
        enemy.set_position(self.start, self.dest, self.speed)

