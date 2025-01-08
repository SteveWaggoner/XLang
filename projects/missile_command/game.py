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

class Position:
    def __init__(self,x,y):
        self.x = WordDecimal().set(x)
        self.y = WordDecimal().set(y)
    def __str__(self):
        return str(round(self.x.get(),2))+","+str(round(self.y.get(),2))

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
        if frame.action == "radius":
            self.item.radius.set(frame.num)
        elif frame.action == "destroy":
            self.item.destroy()

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

class ExplosionAnimation(Animation):

    frames = []
    frames.append(Frame("radius", num=6))
    frames.append(Frame("radius", num=10))
    frames.append(Frame("radius", num=20))
    frames.append(Frame("radius", num=18))
    frames.append(Frame("radius", num=20))
    frames.append(Frame("radius", num=18))
    frames.append(Frame("radius", num=16))
    frames.append(Frame("radius", num=14))
    frames.append(Frame("radius", num=8))
    frames.append(Frame("radius", num=4))
    frames.append(Frame("destroy"))

    def get_frame(self):
        return ExplosionAnimation.frames[self.frame_n.get()]

    def next_frame(self):
        self.frame_n = ( self.frame_n + 1 ) % len(ExplosionAnimation.frames)

class PlaneAnimation(Animation):

    frames = []
    frames.append(Frame("radius", num=5, duration=3))
    frames.append(Frame("radius", num=6, duration=5))
    frames.append(Frame("radius", num=5, duration=1))
    frames.append(Frame("radius", num=4, duration=1))

    def get_frame(self):
        return PlaneAnimation.frames[self.frame_n.get()]

    def next_frame(self):
        self.frame_n = ( self.frame_n + 1 ) % len(PlaneAnimation.frames)


class Graphic:

    def __init__(self):
        # graphical object
        self.graphic = []
        self.animation = None

    def undraw(self):
        for g in self.graphic:
            g.undraw()
        self.graphic = []

    def draw(self, win):

        self.undraw()
        self.render()
        for g in self.graphic:
            g.draw(win)

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


class Item(Graphic):
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

        self.width  = Word()
        self.height = Word()
        self.radius = Word(1)   # all enemys have a radius so just default

        self.route = None
        self.route_n = Byte(0)
        self.last_dodge = Word(0)
        self.destroy_at_dest = Byte(False)

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

    def distance_to(self, other):
        # manhattan distance
      #  return (self.pos.x - other.x).abs() + (self.pos.y - other.y).abs()
        # chebyshev distance
        return max((self.pos.x - other.x).abs(), (self.pos.y - other.y).abs())

    def set_position(self, start, dest=None, speed=None, width=None, height=None):

        self.start = start
        self.pos   = Position(start.x,start.y)

        if not width is None:
            self.width.set(width)
            self.height.set(height)

        if dest:
            self.dest  = dest
            self.speed = speed
            self.update_vectors()


    def update_vectors(self):

        delta_x = (self.dest.x - self.pos.x)
        delta_y = (self.dest.y - self.pos.y)

        rough_distance_in_pixels = delta_x.abs() + delta_y.abs()
        pixels_per_second = self.speed
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

        self.velocity = Position(delta_x_per_tick.get(),delta_y_per_tick.get())


    def move(self):
        self.pos.x = self.pos.x + self.velocity.x
        self.pos.y = self.pos.y + self.velocity.y
        self.distance = self.distance_to(self.dest)


    def destroy(self):
        if self.active:
            self.list.num_active = self.list.num_active - 1
            print("destroyed "+str(self))
            self.active = False
            self.undraw()

    def render(self):
        # dummy
        self.add_circle(self.start.x, self.start.y, Byte(3))


class MissileItem(Item):
    def __init__(self):
        super().__init__()
        self.destroy_at_dest.set(True)

    def render(self):
        self.add_line(self.start.x, self.start.y, self.pos.x, self.pos.y)
        self.add_circle(self.pos.x, self.pos.y, Byte(1))

class BombItem(Item):
    def render(self):
        self.add_line(self.start.x, self.start.y, self.pos.x, self.pos.y)
        self.add_circle(self.pos.x, self.pos.y, Byte(1))

class SmartBombItem(Item):
    def render(self):
        self.add_line(self.pos.x-2, self.pos.y-2, self.pos.x+2, self.pos.y+2)
        self.add_line(self.pos.x+2, self.pos.y-2, self.pos.x-2, self.pos.y+2)
        self.add_circle(self.pos.x, self.pos.y, Byte(1))


class PlaneItem(Item):
    def __init__(self):
        super().__init__()
        self.animation = PlaneAnimation(self)
        self.destroy_at_dest.set(True)

    def render(self):
        self.add_circle(self.pos.x, self.pos.y, self.radius)

class AlienItem(Item):
    def __init__(self):
        super().__init__()
        self.width.set(3)
        self.height.set(3)
        self.destroy_at_dest.set(1)

    def render(self):
        self.add_rectangle(self.pos.x, self.pos.y, self.pos.x+self.width, self.pos.y+self.height)



class ExplosionItem(Item):
    def __init__(self):
        super().__init__()
        self.animation = ExplosionAnimation(self)

    def render(self):
        self.add_circle( self.pos.x, self.pos.y, self.radius)

class BatteryItem(Item):
    def __init__(self):
        super().__init__()
        self.num_missiles = Byte(0)

    def render(self):
        self.add_rectangle(self.pos.x, self.pos.y,
                           self.pos.x + self.width, self.pos.y + self.height)
        self.add_text(self.pos.x + self.width/2, self.pos.y + self.height/2, str(self.num_missiles))


class CityItem(Item):
    def __init__(self):
        super().__init__()
        self.destroyed = Byte(False)

    def render(self):
        if self.destroyed.get():
            self.add_rectangle(self.pos.x, self.pos.y + (self.height-1),
                               self.pos.x+self.width, self.pos.y + self.height)
        else:
            self.add_rectangle(self.pos.x, self.pos.y,
                                self.pos.x + self.width, self.pos.y + self.height)

class LandItem(Item):
    def render(self):
        self.add_rectangle(self.pos.x, self.pos.y,
                           self.pos.x + self.width, self.pos.y + self.height)

class Background(Graphic):
    pass


class Foreground(Graphic):

    def set_fields(self, level, score, game_over, debug):
        self.level = level
        self.score = score
        self.game_over = game_over
        self.debug = debug

    def render(self):
        self.add_text(Byte(60), Byte(20), str(self.debug))
        self.add_text(Byte(180), Byte(10), "level: "+str(self.level)+"   score:" + str(self.score))
        if self.game_over.get():
            self.add_text(Byte(180), Byte(100), "GAME OVER")


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


    def get_collisions_circles(self, other):
        hits = []
        for a in self.items:
            if a.active:
                for b in other.items:
                    if b.active:
                        if a.collide_circles(b):
                            hits.append((a,b))
        return hits

    def get_collisions_pnt_in_rect(self, other):
        hits = []
        for a in self.items:
            if a.active:
                for b in other.items:
                    if b.active:
                        if a.collide_pnt_in_rect(b):
                            hits.append((a,b))
        return hits


class Enemy:

    def __init__(self, enemy, start, speed, dest=None, launch_time=None, attack_times=None, attack_types=None, route=None):
        self.enemy = enemy
        self.start = start
        self.dest = dest
        self.speed = speed

        if not launch_time is None:
            #convert from seconds to ticks (ie. we can increase frame rate and timing doesn't change for level)
            self.launch_time = int(launch_time * TICKS_PER_SECOND)
        if not attack_times is None:
            #convert from seconds to ticks (ie. we can increase frame rate and timing doesn't change for level)
            self.attack_times = [int(s * TICKS_PER_SECOND) for s in attack_times]

        self.attack_types = attack_types
        self.route = route
        if self.dest is None:
            self.dest = self.route.pop(0)

    def spawn(self, game):
        if self.enemy == "bomb":
            enemy = game.bomb.create()
        elif self.enemy == "smartbomb":
            enemy = game.smartbomb.create()
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

class Level:

    def __init__(self):
        self.enemy = []
        self.score_multiplier = 1
        self.backgroud_color = ""


class Game:

    levels = []
    levels.append(Level())
    levels[0].score_multiplier = 1
    levels[0].background_color = "blue"

    levels[0].enemy.append(Enemy("smartbomb",launch_time=0.5,start=Position(x=180,y=0), speed=25, dest=Position(x=255, y=180)))

    levels[0].enemy.append(Enemy("alien",launch_time=3,start=Position(x=0,y=110), speed=25,
                           attack_times=[50,100],attack_types=["single_bomb"],
                           route=[Position(x=50, y=90),Position(x=100, y=50),Position(x=150, y=90),Position(x=320, y=50)]))

    levels[0].enemy.append(Enemy("alien",launch_time=10,start=Position(x=320,y=90), dest=Position(x=0, y=90), speed=25,
                           attack_times=[30,31,32,90,91,92,120,121],attack_types=["single_bomb","multiple_bombs"]))

    levels[0].enemy.append(Enemy("plane",launch_time=11,start=Position(x=320,y=90), dest=Position(x=0, y=90), speed=25,
                           attack_times=[30,31,32,90,91,92,120,121],attack_types=["single_bomb","multiple_bombs"]))

    levels.append(Level())
    levels[1].enemy.append(Enemy("bomb",launch_time=1,start=Position(x=10,y=0), dest=Position(x=55, y=200), speed=15))
    levels[1].enemy.append(Enemy("bomb",launch_time=5,start=Position(x=50,y=0), dest=Position(x=150, y=200), speed=15))
    levels[1].enemy.append(Enemy("bomb",launch_time=6,start=Position(x=70,y=0), dest=Position(x=230, y=200), speed=15))
    levels[1].enemy.append(Enemy("bomb",launch_time=8,start=Position(x=210,y=0), dest=Position(x=255, y=180), speed=15))


    levels.append(Level())
    levels[2].enemy.append(Enemy("bomb",launch_time=1,start=Position(x=10,y=0), dest=Position(x=55, y=200), speed=25))
    levels[2].enemy.append(Enemy("bomb",launch_time=3,start=Position(x=50,y=0), dest=Position(x=150, y=200), speed=25))
    levels[2].enemy.append(Enemy("bomb",launch_time=3,start=Position(x=270,y=0), dest=Position(x=180,y=200), speed=25))
    levels[2].enemy.append(Enemy("bomb",launch_time=3,start=Position(x=210,y=0), dest=Position(x=115,y=180), speed=25))
    levels[2].enemy.append(Enemy("bomb",launch_time=4,start=Position(x=110,y=0), dest=Position(x=115,y=180), speed=25))
    levels[2].enemy.append(Enemy("bomb",launch_time=3,start=Position(x=210,y=0), dest=Position(x=255,y=180), speed=25))
    levels[2].enemy.append(Enemy("bomb",launch_time=4,start=Position(x=110,y=0), dest=Position(x=85,y=180), speed=25))

    levels.append(Level())
    levels[3].enemy.append(Enemy("bomb",launch_time=1,start=Position(x=10,y=0), dest=Position(x=55, y=200), speed=15))
    levels[3].enemy.append(Enemy("bomb",launch_time=3,start=Position(x=15,y=0), dest=Position(x=55, y=200), speed=15))
    levels[3].enemy.append(Enemy("bomb",launch_time=3,start=Position(x=18,y=0), dest=Position(x=55, y=200), speed=15))
    levels[3].enemy.append(Enemy("bomb",launch_time=5,start=Position(x=50,y=0), dest=Position(x=150, y=200), speed=15))
    levels[3].enemy.append(Enemy("bomb",launch_time=5,start=Position(x=54,y=0), dest=Position(x=150, y=200), speed=15))
    levels[3].enemy.append(Enemy("bomb",launch_time=5,start=Position(x=58,y=0), dest=Position(x=150, y=200), speed=15))
    levels[3].enemy.append(Enemy("bomb",launch_time=6,start=Position(x=70,y=0), dest=Position(x=230, y=200), speed=15))
    levels[3].enemy.append(Enemy("bomb",launch_time=6,start=Position(x=72,y=0), dest=Position(x=230, y=200), speed=15))
    levels[3].enemy.append(Enemy("bomb",launch_time=6,start=Position(x=73,y=0), dest=Position(x=230, y=200), speed=15))
    levels[3].enemy.append(Enemy("bomb",launch_time=8,start=Position(x=210,y=0), dest=Position(x=255, y=180), speed=15))
    levels[3].enemy.append(Enemy("bomb",launch_time=8,start=Position(x=211,y=0), dest=Position(x=255, y=180), speed=15))
    levels[3].enemy.append(Enemy("bomb",launch_time=8,start=Position(x=218,y=0), dest=Position(x=255, y=180), speed=15))


    def __init__(self):

        self.clock       = Word(0)
        self.sleep_until = Word(0)
        self.level_step  = None
        self.enemy_n     = Byte(0)

        self.fps = ""

        self.game_over = Byte(False)
        self.graphic = []
        self.score = DWord(0)
        self.next_city_score = Word(10000)

        self.background = Background()
        self.foreground = Foreground()

        self.missile   = ItemList(MissileItem,15)
        self.bomb      = ItemList(BombItem,25)
        self.smartbomb = ItemList(SmartBombItem,4)
        self.plane     = ItemList(PlaneItem,4)
        self.alien     = ItemList(AlienItem,4)
        self.explosion = ItemList(ExplosionItem,15)

        self.init_land()
        self.init_cities()
        self.init_batteries()

        self.win = GraphWin(width = 960, height = 600, autoflush = False) # create a window
        self.win.setCoords(0, 200, 320, 0) # set the coordinates of the window (mimic VGA)


    def init_land(self):
        self.land = ItemList(LandItem, 1, True)
        self.land[0].set_position(Position(x=0, y=185),width=320, height=15)

    def init_cities(self):

        self.city = ItemList(CityItem, 6, True)
        self.city[0].set_position(Position(x =  46, y=180), width=20,height=5)
        self.city[1].set_position(Position(x =  78, y=180), width=20,height=5)
        self.city[2].set_position(Position(x = 108, y=180), width=20,height=5)
        self.city[3].set_position(Position(x = 172, y=180), width=20,height=5)
        self.city[4].set_position(Position(x = 210, y=180), width=20,height=5)
        self.city[5].set_position(Position(x = 246, y=180), width=20,height=5)

    def init_batteries(self):

        self.battery = ItemList(BatteryItem, 3, True)
        self.battery[0].set_position(Position(x= 12,y=176), width=28,height=10)
        self.battery[1].set_position(Position(x=140,y=176), width=28,height=10)
        self.battery[2].set_position(Position(x=280,y=176), width=28,height=10)
        self.active_battery_n = 1


    def load_level(self, level_n):

        print("starting level...")
        playsound("sounds/alert.mp3", False)

        self.clock.set(0)
        self.sleep_until.set(0)
        self.enemy_n.set(0)

        self.active_level_n = level_n
        self.active_level = Game.levels[level_n]

        self.missile.clear()
        self.bomb.clear()

        for b in range(3):
            self.battery[b].num_missiles.set(10)

        print("done load_level")

    target_n=0
    def get_random_target(self):
        targets = [Position(x=55, y=200),
                   Position(x=150, y=200),
                   Position(x=180,y=200),
                   Position(x=115,y=180),
                   Position(x=255,y=180),
                   Position(x=85,y=180)
                   ]
        Game.target_n = ( Game.target_n + 1 ) % len(targets)
        return targets[Game.target_n]


    def launch_missile(self, battery_n, dest_x, dest_y, speed):

        battery = self.battery[battery_n]

        if dest_y > battery.pos.y:
            print("invalid launch coord")
            return

        if battery.num_missiles < 1:
            print("no missiles")
            return

        playsound("sounds/missile-fire.mp3", False)

        missile = self.missile.create()
        start_x = battery.pos.x + (battery.width/2)
        start_y = battery.pos.y

        missile.set_position(Position(start_x,start_y),Position(dest_x,dest_y), speed)

        battery.num_missiles = battery.num_missiles - 1


    def create_explosion(self, pos):

        e = self.explosion.create()
        e.set_position(pos)


    def create_attack(self, plane, attack_type):

        if attack_type == "single_bomb":
            target = self.get_random_target()
            enemy = Enemy(enemy="bomb", start=Position(plane.pos.x,plane.pos.y), dest=target, speed=25)
            enemy.spawn(self)
        elif attack_type == "multiple_bombs":
            for i in range(3):
                target = self.get_random_target()
                enemy = Enemy(enemy="bomb", start=Position(plane.pos.x+i,plane.pos.y+i), dest=target, speed=25)
                enemy.spawn(self)
        else:
            print("unknown attack type: "+attack_type)

    def score_level(self):
        print("score_level")
        for battery in self.battery.items:
            self.score = self.score + (5 * battery.num_missiles.get()) # 5 points per unused missile


        for city in self.city.items:
            if not city.destroyed.get():
                self.score = self.score + (200)  # 100 points per saved city

        if self.score.get() >= self.next_city_score.get():
            for city in self.city.items:
                if city.destroyed.get():
                    city.destroyed.set(False)
                    break

        valid_cities = 0
        for city in self.city.items:
            if not city.destroyed.get():
                valid_cities = valid_cities + 1

        if valid_cities == 0:
            self.game_over.set(True)

    def next_level(self):
        print("next_level")
        self.load_level((self.active_level_n + 1) % len(Game.levels))


    def game_input(self):

        pnt = self.win.checkMouse()
        if not pnt is None:
            self.launch_missile(self.active_battery_n, int(pnt.x), int(pnt.y), 80)

        key = self.win.checkKey()
        if key == "1":
            self.active_battery_n = 0
        if key == "2":
            self.active_battery_n = 1
        if key == "3":
            self.active_battery_n = 2


    def sleep(self, seconds):
        self.sleep_until = self.clock + int(seconds * TICKS_PER_SECOND)

    def is_sleeping(self):
        return self.sleep_until > self.clock

    def dodge_nearby_explosions(self, enemy):
        for explosion in self.explosion.items:
            if explosion.active:
                if explosion.distance_to(enemy.pos) < 90 and enemy.last_dodge + 5 < self.clock:
                    enemy.last_dodge = self.clock
                    if enemy.route:
                        enemy.route.insert(enemy.route_n.get(), enemy.dest)
                    else:
                        enemy.route = [enemy.dest]
                    enemy.dest = Position(enemy.pos.x + (enemy.velocity.x * 6), enemy.pos.y - (enemy.velocity.y * 8))
                    enemy.update_vectors()
                    break


    def move_items(self, collection, enable_attack=False, enable_explode=False, enable_dodge=False):

        for item in collection.items:
            if item.active:
                item.move()

                if enable_attack and item.attack_times:
                    if self.clock in item.attack_times:
                        attack_n = item.attack_times.index(self.clock)
                        attack_type = item.attack_types[attack_n % len(item.attack_types)]
                        self.create_attack(item, attack_type)

                at_dest = item.distance < 5
                if at_dest:

                    if item.route and item.route_n < len(item.route):
                        next_dest = item.route[item.route_n.get()]
                        item.route_n = item.route_n + 1
                        item.dest = next_dest
                        item.update_vectors()
                    else:
                        if enable_explode:
                            self.create_explosion(item.pos)
                        if item.destroy_at_dest == True:
                            item.destroy()

                if enable_dodge:
                    if self.explosion.num_active > 0:
                        self.dodge_nearby_explosions(item)



    def explode_enemy(self, enemy, score_points):
        bombs_hit = self.explosion.get_collisions_circles(enemy)
        for explosion, enemy in bombs_hit:
            self.score = self.score + score_points
            enemy.destroy()
            playsound("sounds/explosions.mp3", False)


    def game_tick(self):

        #
        # process the end of level in step (let physics continue but update score)
        #
        if not self.is_sleeping():

            #
            # run the level
            #
            if self.enemy_n < len(self.active_level.enemy):
                level_enemy = self.active_level.enemy[self.enemy_n.get()]
                if level_enemy.launch_time < self.clock:
                    level_enemy.spawn(self)
                    self.enemy_n = self.enemy_n + 1

            #
            # if the game not over
            #
            if self.game_over == False:
                level_over = self.active_level.enemy[-1].launch_time < self.clock \
                        and self.bomb.num_active == 0 \
                        and self.plane.num_active == 0
                if lever_over:

                    if self.level_step == None:
                        self.level_step = "score_level"
                        self.sleep(1.5)
                    elif self.level_step == "score_level":
                        self.score_level()
                        self.level_step = "next_level"
                        self.sleep(1.5)
                    elif self.level_step == "next_level":
                        self.level_step = None
                        self.next_level()


        #
        # Physics
        #
        self.move_items(self.bomb)
        self.move_items(self.smartbomb, enable_dodge=True)
        self.move_items(self.plane, enable_attack=True)
        self.move_items(self.alien, enable_attack=True)
        self.move_items(self.missile, enable_explode=True)

        self.explode_enemy(self.bomb, 25)
        self.explode_enemy(self.plane, 100)
        self.explode_enemy(self.alien, 100)
        self.explode_enemy(self.smartbomb, 125)


        cities_hit = self.bomb.get_collisions_pnt_in_rect(self.city) + self.smartbomb.get_collisions_pnt_in_rect(self.city)
        for bomb, city in cities_hit:
            if city.destroyed == False:
                print("city destroyed")
                city.destroyed.set(True)
                bomb.destroy()
                playsound("sounds/city-blow-up.mp3", False)

        batteries_hit = self.bomb.get_collisions_pnt_in_rect(self.battery) + self.smartbomb.get_collisions_pnt_in_rect(self.battery)
        for bomb, battery in batteries_hit:
            if battery.num_missiles>0:
                battery.num_missiles.set(0)
                playsound("sounds/city-blow-up.mp3", False)

        bombs_hit = self.bomb.get_collisions_pnt_in_rect(self.land) + self.smartbomb.get_collisions_pnt_in_rect(self.land)
        for bomb,land in bombs_hit:
            bomb.destroy()

        self.clock = self.clock + 1

    def draw_items(self, collection):
        for item in collection.items:
            if item.active == True:
                if item.animation:
                    item.animation.tick()
                    if item.active == True:
                        item.draw(self.win)
                else:
                    item.draw(self.win)


    def game_draw(self):

        self.background.draw(self.win)

        self.draw_items(self.land)
        self.draw_items(self.city)
        self.draw_items(self.battery)
        self.draw_items(self.missile)
        self.draw_items(self.bomb)
        self.draw_items(self.smartbomb)
        self.draw_items(self.plane)
        self.draw_items(self.alien)
        self.draw_items(self.explosion)

        self.foreground.set_fields(level=self.active_level_n+1, score=self.score, game_over=self.game_over, debug=self.fps)
        self.foreground.draw(self.win)

        self.win.flush()
        self.win.redraw()


    def is_game_active(self):
        return self.game_over == False or \
               self.missile.num_active > 0 or \
               self.explosion.num_active > 0 or \
               self.bomb.num_active > 0 or \
               self.plane.num_active > 0 or \
               self.alien.num_active > 0 or \
               self.smartbomb.num_active > 0

    def game_loop(self):

        frames = 0
        loop_start = time.time()
        extra_sleep = 0
        wait_secs = 0

        while self.is_game_active():

            #
            # run the game
            #
            start_time = time.time() - extra_sleep
            self.game_input()
            self.game_tick()
            self.game_draw()
            end_time = time.time()

            #
            # wait so we have consistent FPS in loop (note: sleep is slightly broken so measure extra sleep)
            #
            sleep_start = time.time()
            wait_secs = start_time + SECONDS_PER_TICK - end_time
            if wait_secs > 0:
                time.sleep(wait_secs)
            sleep_end = time.time()
            extra_sleep = sleep_end - sleep_start - wait_secs #python sleep is longer than requested?1?

            #
            # statistics for tuning and debugging
            #
            frames = frames + 1
            duration = time.time()-loop_start
            if frames % 5 == 1:
                self.fps = "fps: " + str(round(frames/duration,3)) + "  wait "+str(round(wait_secs,3))+" frames="+str(frames)


xgame = Game()
xgame.load_level(0)
xgame.game_loop()
xgame.win.getKey()

