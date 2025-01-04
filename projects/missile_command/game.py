#!/usr/bin/python3.9

# https://stackoverflow.com/questions/15886455/simple-graphics-for-python
from graphics import GraphWin, Rectangle, Point, Circle, Line, Text
from playsound import playsound
import time
import math


SECONDS_PER_TICK=0.08
TICKS_PER_SECOND=int(1.0/SECONDS_PER_TICK)

class Position:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Frame:
    def __init__(self, action, next_tick=1, num=None):
        self.next_tick = next_tick
        self.action = action
        self.num = num

class Animation:

    def __init__(self, item):
        self.item    = item
        self.frame_n = 0

    def reset(self):
        self.frame_n = 0

    def get_frame(self):
        return None

    def next_frame(self):
        pass

    def tick(self):

        frame = self.get_frame()
        if frame:
            if frame.action == "radius":
                self.item.radius = frame.num
            elif frame.action == "destroy":
                self.item.destroy()
            self.next_frame()

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
        return ExplosionAnimation.frames[self.frame_n]

    def next_frame(self):
        self.frame_n = ( self.frame_n + 1 ) % len(ExplosionAnimation.frames)



class Item:
    def __init__(self):

        # memory allocation
        self.active = False

        #location and size
        self.start = None   # origin of missile/bomb
        self.pos   = None
        self.dest  = None

        self.width  = None
        self.height = None
        self.radius = 1

        # graphical object
        self.graphic = []
        self.animation = None


    def collide_circles(self, other):
        diff_x = abs(self.pos.x - other.pos.x)
        if diff_x < self.radius + other.radius:
            diff_y = abs(self.pos.y - other.pos.y)
            if diff_y < self.radius + other.radius:
                return True
        return False

    def collide_pnt_in_rect(self, other):

        if self.pos.x > other.pos.x and self.pos.x < other.pos.x + other.width:
            if self.pos.y > other.pos.y and self.pos.y < other.pos.y + other.height:
                return True
        return False

    def distance_to(self, other):
        # manhattan_distance
        #return abs(self.x - other_x) + abs(self.y - other_y)

        # real
        return math.sqrt(((self.pos.x - other.x)*(self.pos.x - other.x)) + ((self.pos.y - other.y)*(self.pos.y - other.y)))

    def set_position(self, start, dest=None, speed=None, width=None, height=None):

        self.start = start
        self.pos   = Position(start.x,start.y)
        self.width = width
        self.height= height

        if dest:

            self.dest  = dest
            self.speed = speed

            self.distance = self.distance_to(self.dest)

            seconds_until_dest = (self.distance / self.speed)
            ticks_until_dest = seconds_until_dest * TICKS_PER_SECOND
            delta_x = self.dest.x - self.pos.x
            delta_y = self.dest.y - self.pos.y

            delta_x_per_tick = delta_x / ticks_until_dest
            delta_y_per_tick = delta_y / ticks_until_dest

            self.velocity = Point(delta_x_per_tick,delta_y_per_tick)

            print("self.distance = "+str(self.distance))
            print("self.speed = "+str(self.speed))
            print("seconds_until_dest = "+str(seconds_until_dest))
            print("ticks_until_dest = "+str(ticks_until_dest))
            print("self.velocity = "+str(self.velocity))


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


    def undraw(self):
        for g in self.graphic:
            g.undraw()
        self.graphic = []

    def draw(self, win):

        self.undraw()
        self.render()
        for g in self.graphic:
            g.draw(win)

    def render(self):
        # default to rectangle
        self.graphic.append(Rectangle(Point(self.pos.x, self.pos.y),
                                      Point(self.pos.x+self.width, self.pos.y+self.height)))



class MissileItem(Item):
    def render(self):
        self.graphic.append(Line(Point(self.start.x, self.start.y),
                                 Point(self.pos.x, self.pos.y)))
        self.graphic.append(Circle(Point(self.pos.x,self.pos.y), 1))

class BombItem(Item):
    def render(self):
        self.graphic.append(Line(Point(self.start.x, self.start.y),
                                 Point(self.pos.x, self.pos.y)))
        self.graphic.append(Circle(Point(self.pos.x, self.pos.y), 1))

class ExplosionItem(Item):
    def __init__(self):
        super().__init__()
        self.animation = ExplosionAnimation(self)

    def render(self):
        self.graphic.append( Circle(Point(self.pos.x, self.pos.y), self.radius) )

class BatteryItem(Item):
    def render(self):
        self.graphic.append(Rectangle(Point(self.pos.x, self.pos.y),
                                      Point(self.pos.x+self.width, self.pos.y+self.height)))
        self.graphic.append(Text(Point(self.pos.x + self.width/2, self.pos.y + self.height/2), str(self.num_missiles)))


class CityItem(Item):
    def __init__(self):
        super().__init__()
        self.destroyed = False

    def render(self):
        if self.destroyed:
            self.graphic.append(Rectangle(Point(self.pos.x, self.pos.y+(self.height-1)),
                                          Point(self.pos.x+self.width, self.pos.y+self.height)))
        else:
            self.graphic.append(Rectangle(Point(self.pos.x, self.pos.y),
                                          Point(self.pos.x+self.width, self.pos.y+self.height)))

class LandItem(Item):
    pass


class ItemList:

    def __init__(self, item_class, max_items, active=False):

        self.num_active = 0
        self.next_alloc = 0
        self.items = []
        for x in range(max_items):
            i = item_class()
            i.list = self
            i.active = active
            self.items.append(i)

    def __getitem__(self, key):
        return self.items[key]

    def create(self):

        n = self.next_alloc
        i = 0

        while i < len(self.items):
            if not self.items[n].active:
                self.items[n].active = True
                self.next_alloc = ( n + 1 ) % len(self.items)
                self.num_active = self.num_active + 1
                print("created "+str(self.items[n])+" "+str(n))
                return self.items[n]
            i = i + 1
            n = (n + 1) % len(self.items)

        print("bad alloc")
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


class LevelBomb:

    def __init__(self, launch_time, start, dest, speed):
        self.launch_time = launch_time
        self.start = start
        self.dest = dest
        self.speed = speed


class Game:

    levels = []
    levels.append([])
    levels[0].append(LevelBomb(launch_time=1,start=Position(x=10,y=0), dest=Position(x=55, y=200), speed=15))
    levels[0].append(LevelBomb(launch_time=50,start=Position(x=50,y=0), dest=Position(x=150, y=200), speed=15))
    levels[0].append(LevelBomb(launch_time=60,start=Position(x=70,y=0), dest=Position(x=230, y=200), speed=15))
    levels[0].append(LevelBomb(launch_time=80,start=Position(x=210,y=0), dest=Position(x=255, y=180), speed=15))

    levels.append([])
    levels[1].append(LevelBomb(launch_time=1,start=Position(x=10,y=0), dest=Position(x=55, y=200), speed=25))
    levels[1].append(LevelBomb(launch_time=30,start=Position(x=50,y=0), dest=Position(x=150, y=200), speed=25))
    levels[1].append(LevelBomb(launch_time=30,start=Position(x=270,y=0), dest=Position(x=180,y=200), speed=25))
    levels[1].append(LevelBomb(launch_time=30,start=Position(x=210,y=0), dest=Position(x=115,y=180), speed=25))
    levels[1].append(LevelBomb(launch_time=40,start=Position(x=110,y=0), dest=Position(x=115,y=180), speed=25))
    levels[1].append(LevelBomb(launch_time=30,start=Position(x=210,y=0), dest=Position(x=255,y=180), speed=25))
    levels[1].append(LevelBomb(launch_time=40,start=Position(x=110,y=0), dest=Position(x=85,y=180), speed=25))

    levels.append([])
    levels[2].append(LevelBomb(launch_time=1,start=Position(x=10,y=0), dest=Position(x=55, y=200), speed=15))
    levels[2].append(LevelBomb(launch_time=32,start=Position(x=15,y=0), dest=Position(x=55, y=200), speed=15))
    levels[2].append(LevelBomb(launch_time=34,start=Position(x=18,y=0), dest=Position(x=55, y=200), speed=15))
    levels[2].append(LevelBomb(launch_time=50,start=Position(x=50,y=0), dest=Position(x=150, y=200), speed=15))
    levels[2].append(LevelBomb(launch_time=52,start=Position(x=54,y=0), dest=Position(x=150, y=200), speed=15))
    levels[2].append(LevelBomb(launch_time=54,start=Position(x=58,y=0), dest=Position(x=150, y=200), speed=15))
    levels[2].append(LevelBomb(launch_time=60,start=Position(x=70,y=0), dest=Position(x=230, y=200), speed=15))
    levels[2].append(LevelBomb(launch_time=63,start=Position(x=72,y=0), dest=Position(x=230, y=200), speed=15))
    levels[2].append(LevelBomb(launch_time=66,start=Position(x=73,y=0), dest=Position(x=230, y=200), speed=15))
    levels[2].append(LevelBomb(launch_time=80,start=Position(x=210,y=0), dest=Position(x=255, y=180), speed=15))
    levels[2].append(LevelBomb(launch_time=88,start=Position(x=211,y=0), dest=Position(x=255, y=180), speed=15))
    levels[2].append(LevelBomb(launch_time=89,start=Position(x=218,y=0), dest=Position(x=255, y=180), speed=15))


    def __init__(self):

        self.clock     = 0
        self.wait_until = 0
        self.level_step = None

        self.game_over = False
        self.graphic = []
        self.score = 0
        self.next_city_score = 10000

        self.missile   = ItemList(MissileItem,30)
        self.bomb      = ItemList(BombItem,30)
        self.explosion = ItemList(ExplosionItem,30)

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

        self.clock = 0

        self.active_level_n = level_n
        self.active_level = Game.levels[level_n]

        self.missile.clear()
        self.bomb.clear()

        for b in range(3):
            self.battery[b].num_missiles = 10


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


    def score_level(self):
        print("score_level")
        for battery in self.battery.items:
            self.score = self.score + (5 * battery.num_missiles) # 5 points per unused missile


        for city in self.city.items:
            if not city.destroyed:
                self.score = self.score + (200)  # 100 points per saved city

        if self.score >= self.next_city_score:
            for city in self.city.items:
                if city.destroyed:
                    city.destroyed = False
                    break

        valid_cities = 0
        for city in self.city.items:
            if not city.destroyed:
                valid_cities = valid_cities + 1

        if valid_cities == 0:
            self.game_over = True

    def next_level(self):
        print("next_level")
        self.load_level((self.active_level_n + 1) % len(Game.levels))


    def game_input(self):
        pnt = self.win.checkMouse()
        if not pnt is None:
            self.launch_missile(self.active_battery_n, pnt.x, pnt.y, 80)

        key = self.win.checkKey()
        if key == "1":
            self.active_battery_n = 0
        if key == "2":
            self.active_battery_n = 1
        if key == "3":
            self.active_battery_n = 2


    def wait(self, seconds):
        self.wait_until = self.clock + (seconds * TICKS_PER_SECOND)

    def is_waiting(self):
        return self.wait_until > self.clock

    def game_update(self):


        #
        # run the level
        #
        for level_bomb in self.active_level:
            if level_bomb.launch_time == self.clock:
                bomb = self.bomb.create()
                bomb.set_position(level_bomb.start,level_bomb.dest, level_bomb.speed)

        #
        # if the game not over
        #
        if not self.game_over:


            #
            # process the end of level in step (let physics continue but update score)
            #
            if not self.is_waiting():

                is_level_over = self.active_level[-1].launch_time < self.clock and self.bomb.num_active == 0
                if self.level_step == None and is_level_over:
                    self.level_step = "score_level"
                    self.wait(0.5)
                elif self.level_step == "score_level":
                    self.score_level()
                    self.level_step = "next_level"
                    self.wait(0.5)
                elif self.level_step == "next_level":
                    self.level_step = None
                    self.next_level()


        #
        # Physics
        #
        for bomb in self.bomb.items:
            if bomb.active:
                bomb.move()

        for missile in self.missile.items:
            if missile.active:
                missile.move()
                if missile.distance < 5:
                    self.create_explosion(missile.pos)
                    missile.destroy()

        bombs_hit = self.explosion.get_collisions_circles(self.bomb)
        for explosion, bomb in bombs_hit:
            self.score = self.score + 25 #destroy dumb bombs = 25 points
            bomb.destroy()
            playsound("sounds/explosions.mp3", False)


        cities_hit = self.bomb.get_collisions_pnt_in_rect(self.city)
        for bomb, city in cities_hit:
            if not city.destroyed:
                print("city destroyed")
                city.destroyed = True
                bomb.destroy()
                playsound("sounds/city-blow-up.mp3", False)

        batteries_hit = self.bomb.get_collisions_pnt_in_rect(self.battery)
        for bomb, battery in batteries_hit:
            if battery.num_missiles>0:
                battery.num_missiles = 0
                playsound("sounds/city-blow-up.mp3", False)

        bombs_hit = self.bomb.get_collisions_pnt_in_rect(self.land)
        for bomb,land in bombs_hit:
            bomb.destroy()

        self.clock = self.clock + 1

    def draw_score(self, win):

        for g in self.graphic:
            g.undraw()
        self.graphic = []
        self.graphic.append(Text(Point(180, 10), "level: "+str(self.active_level_n + 1)+"   score:" + str(self.score)))
        if self.game_over:
            self.graphic.append(Text(Point(180, 100), "GAME OVER"))

        for g in self.graphic:
            g.draw(win)


    def game_draw(self):

        for land in self.land.items:
            land.draw(self.win)

        for city in self.city.items:
            city.draw(self.win)

        for battery in self.battery.items:
            battery.draw(self.win)

        for missile in self.missile.items:
            if missile.active:
                missile.draw(self.win)

        for bomb in self.bomb.items:
            if bomb.active:
                bomb.draw(self.win)

        for explosion in self.explosion.items:
            if explosion.active:
                explosion.animation.tick()
                if explosion.active:
                    explosion.draw(self.win)

        self.draw_score(self.win)

        self.win.flush()
        self.win.redraw()


    def is_game_active(self):
        return not self.game_over or self.missile.num_active > 0 or self.explosion.num_active > 0 or self.bomb.num_active > 0

    def game_loop(self):

        while self.is_game_active():

            start_time = time.time()
            self.game_input()
            self.game_update()
            self.game_draw()
            end_time = time.time()

            wait_secs = start_time + SECONDS_PER_TICK - end_time
            if wait_secs > 0:
                time.sleep(wait_secs)

xgame = Game()
xgame.load_level(0)
xgame.game_loop()
xgame.win.getKey()

