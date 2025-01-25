#!/usr/bin/python3.9

from c6502 import Byte, Word, WordDecimal
from object import Position, Action, Object
from clock import Clock


class Object_Missile(Object):
    def __init__(self):
        super().__init__()
        self.destroy_at_dest.set(True)


class Object_Bomb(Object):
    pass

class Object_SmartBomb(Object):
    pass


class Object_Plane(Object):
    def __init__(self):
        super().__init__()

        self.actions = []
        self.actions.append(Action(Action.set_radius, num=3, duration=0.2))
        self.actions.append(Action(Action.set_radius, num=6, duration=0.2))
        self.actions.append(Action(Action.set_radius, num=9, duration=0.2))
        self.actions.append(Action(Action.set_radius, num=6, duration=0.2))

        self.destroy_at_dest.set(True)


class Object_Alien(Object):
    def __init__(self):
        super().__init__()
        self.width.set(3)
        self.height.set(3)
        self.destroy_at_dest.set(1)


class Object_Mario(Object):
    def __init__(self):
        super().__init__()
        self.width.set(3)
        self.height.set(3)



class Object_Explosion(Object):
    def __init__(self):
        super().__init__()

        self.actions = []
        self.actions.append(Action(Action.set_radius, num=6))
        self.actions.append(Action(Action.set_radius, num=10))
        self.actions.append(Action(Action.set_radius, num=20))
        self.actions.append(Action(Action.set_radius, num=18))
        self.actions.append(Action(Action.set_radius, num=20))
        self.actions.append(Action(Action.set_radius, num=18))
        self.actions.append(Action(Action.set_radius, num=16))
        self.actions.append(Action(Action.set_radius, num=14))
        self.actions.append(Action(Action.set_radius, num=8))
        self.actions.append(Action(Action.set_radius, num=4))
        self.actions.append(Action(Action.destroy))



class Object_Battery(Object):
    def __init__(self):
        super().__init__()
        self.num_missiles = Byte(0)
        self.selected = Byte(0)

    def destroy(self):
        self.num_missiles.set(0)


class Object_City(Object):
    def __init__(self):
        super().__init__()
        self.destroyed = Byte(False)

    def destroy(self):
        self.destroyed.set(True)


class Object_Land(Object):
    pass


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

