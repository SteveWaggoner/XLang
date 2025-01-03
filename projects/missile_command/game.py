#!/usr/bin/python3.9

# https://stackoverflow.com/questions/15886455/simple-graphics-for-python
from graphics import GraphWin, Rectangle, Point, Circle, Line

import time


class State:
    def __init__(self, next_state, action, num=None):
        self.next_state = next_state
        self.action = action
        self.num = num

class StateMachine:

    states = {}
    states[1]  = State(2,  "radius", 2)
    states[2]  = State(3,  "radius", 6)
    states[3]  = State(4,  "radius", 10)
    states[4]  = State(5,  "radius", 14)
    states[5]  = State(6,  "radius", 18)
    states[6]  = State(7,  "radius", 16)
    states[7]  = State(8,  "radius", 10)
    states[8]  = State(9,  "radius", 4)
    states[9]  = State(10, "radius", 3)
    states[10] = State(11, "radius", 2)
    states[11] = State(None, "destroy")

    def __init__(self, item):

        self.item  = item
        self.reset()

    def reset(self):
        if self.item.item_type == "explosion":
            self.state = StateMachine.states[1] #initial state
        else:
            self.state = None


    def tick(self):

        if not self.state is None:
            if self.state.action == "radius":
                self.item.radius = self.state.num
                print("radius="+str(self.item.radius))
            elif self.state.action == "destroy":
                self.item.destroy()
            self.state = StateMachine.states.get(self.state.next_state)



class Item:
    def __init__(self, item_type, active=False):

        # memory allocation
        self.item_type = item_type
        self.active = active

        #location and size
        self.start_x = -1   # origin of missile/bomb
        self.start_y = -1   # origin of missile/bomb
        self.x = -1
        self.y = -1
        self.width = -1
        self.height = -1

        # graphical object
        self.graphic = []

        # object specific
        self.state = None        # for cities
        self.num_missiles = None # for batteries
        self.radius = 1          # for explosions/collision detection
        self.time_to_live = None # for explosions

        # animation support
        if item_type == "explosion":
            self.state_machine = StateMachine(self)


    def collide_circles(self, other):
        diff_x = abs(self.x - other.x)
        if diff_x < self.radius + other.radius:
            diff_y = abs(self.y - other.y)
            if diff_y < self.radius + other.radius:
                return True
        return False

    def collide_pnt_in_rect(self, other):

        if self.x > other.x and self.x < other.x + other.width:
            if self.y > other.y and self.y < other.y + other.height:
                return True
        return False

    def manhattan_distance(self, other_x, other_y):
        return abs(self.x - other_x) + abs(self.y - other_y)

    def update_speed_vectors(self):

        if self.x == -1:
            self.x = self.start_x
            self.y = self.start_y

        self.distance = self.manhattan_distance(self.dest_x, self.dest_y)
        time_req = self.distance / self.speed

        delta_x = self.dest_x - self.x
        delta_y = self.dest_y - self.y

        self.speed_x = delta_x / time_req
        self.speed_y = delta_y / time_req

    def update_position(self):

        self.x = self.x + self.speed_x
        self.y = self.y + self.speed_y
        self.distance = self.manhattan_distance(self.dest_x, self.dest_y)



    def draw(self, win):

        for g in self.graphic:
            g.undraw()
        self.graphic = []

        if self.item_type == "explosion":
            self.graphic.append( Circle(Point(self.x, self.y), self.radius) )
        elif self.item_type == "missile" or self.item_type == "bomb":
            self.graphic.append(Line(Point(self.start_x, self.start_y), Point(self.x, self.y)))
            self.graphic.append(Circle(Point(self.x,self.y), 1))
        elif self.item_type == "city":
            if self.state == "destroyed":
                self.graphic.append(Rectangle(Point(self.x, self.y+(self.height-1)), Point(self.x+self.width, self.y+self.height)))
            else:
                self.graphic.append(Rectangle(Point(self.x, self.y), Point(self.x+self.width, self.y+self.height)))
        else:
            self.graphic.append(Rectangle(Point(self.x, self.y), Point(self.x+self.width, self.y+self.height)))

        for g in self.graphic:
            g.draw(win)

    def destroy(self):
        if self.active:
            print("destroyed "+self.item_type)
            self.active = False
            for g in self.graphic:
                g.undraw()
            self.graphic = []


class ItemList:

    def __init__(self, item_type, max_items, alloc_all=False):

        self.next_alloc = 0
        self.items = []
        for x in range(max_items):
            i = Item(item_type, alloc_all)
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

                print("created "+self.items[n].item_type+" "+str(n))
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

    def __init__(self, launch_time, start_x, start_y, dest_x, dest_y, speed):
        self.launch_time = launch_time
        self.start_x = start_x
        self.start_y = start_y
        self.dest_x = dest_x
        self.dest_y = dest_y
        self.speed = speed


class Game:

    levels = {}
    levels[1] = []
    levels[1].append(LevelBomb(launch_time=30,start_x=10, start_y=0, dest_x=55, dest_y=200, speed=5))
    levels[1].append(LevelBomb(launch_time=60,start_x=50, start_y=0, dest_x=150, dest_y=200, speed=5))
    levels[1].append(LevelBomb(launch_time=90,start_x=70, start_y=0, dest_x=220, dest_y=200, speed=5))
    levels[1].append(LevelBomb(launch_time=120,start_x=210, start_y=0, dest_x=150, dest_y=200, speed=5))
    levels[1].append(LevelBomb(launch_time=160,start_x=110, start_y=0, dest_x=160, dest_y=200, speed=5))
    levels[1].append(LevelBomb(launch_time=165,start_x=110, start_y=0, dest_x=78, dest_y=200, speed=5))
    levels[1].append(LevelBomb(launch_time=170,start_x=110, start_y=0, dest_x=146, dest_y=200, speed=5))
    levels[1].append(LevelBomb(launch_time=180,start_x=110, start_y=0, dest_x=250, dest_y=200, speed=5))

    def __init__(self):

        self.clock     = 0

        self.missile   = ItemList("missile",30)
        self.bomb      = ItemList("bomb",30)
        self.explosion = ItemList("explosion",30)

        self.init_land()
        self.init_cities()
        self.init_batteries()

        self.win = GraphWin(width = 960, height = 600) # create a window
        self.win.setCoords(0, 200, 320, 0) # set the coordinates of the window (mimic VGA)


    def init_land(self):
        self.land = ItemList("land", 1, True)
        self.land[0].x = 0
        self.land[0].y = 185
        self.land[0].width = 320
        self.land[0].height = 15

    def init_cities(self):

        self.city    = ItemList("city", 6, True)
        for c in self.city.items:
            c.width  = 20
            c.height = 5
            c.y      = 180

        self.city[0].x = 46
        self.city[1].x = 78
        self.city[2].x = 108
        self.city[3].x = 172
        self.city[4].x = 210
        self.city[5].x = 246

    def init_batteries(self):

        self.battery = ItemList("battery", 3, True)
        for b in self.battery.items:
            b.width  = 28
            b.height = 10
            b.y      = 176

        self.battery[0].x = 12
        self.battery[1].x = 140
        self.battery[2].x = 280

    def load_missiles(self):

        self.missile.clear()
        for b in range(3):
            self.battery[b].num_missiles = 10


    def load_level(self, level_n):

        self.game_clock = 0

        self.level = Game.levels[level_n]

        self.missile.clear()
        self.bomb.clear()


    def level_tick(self):

        for lb in self.level:
            if lb.launch_time == self.clock:
                b = self.bomb.create()
                b.start_x = lb.start_x
                b.start_y = lb.start_y
                b.x       = -1
                b.y       = -1
                b.dest_x  = lb.dest_x
                b.dest_y  = lb.dest_y
                b.speed   = lb.speed
                b.update_speed_vectors()


    def launch_missile(self, battery_n, dest_x, dest_y, speed):

        battery = self.battery[battery_n]

        if dest_y > battery.y:
            print("invalid launch coord")
            return

        m = self.missile.create()
        m.start_x = battery.x + (battery.width/2)
        m.start_y = battery.y
        m.x = -1
        m.y = -1

        m.launch_time = self.clock
        m.dest_x      = dest_x
        m.dest_y      = dest_y
        m.speed       = speed

        m.update_speed_vectors()


    def create_explosion(self, x, y):

        e = self.explosion.create()
        e.x = x
        e.y = y
        e.state_machine.reset()



    def tick(self):

        self.level_tick()

        for b in self.bomb.items:
            if b.active:
                b.update_position()

        for m in self.missile.items:
            if m.active:
                m.update_position()
                if m.distance < 5:
                    self.create_explosion(m.x,m.y)
                    m.destroy()

        bombs_hit = self.explosion.get_collisions_circles(self.bomb)
        for e,b in bombs_hit:
            b.destroy()

        cities_hit = self.bomb.get_collisions_pnt_in_rect(self.city)
        for b,c in cities_hit:
            print("city destroyed")
            c.state = "destroyed"
            b.destroy()

        batteries_hit = self.bomb.get_collisions_pnt_in_rect(self.battery)
        for b,bat in batteries_hit:
            bat.num_missiles = 0

        bombs_hit = self.bomb.get_collisions_pnt_in_rect(self.land)
        for b,l in bombs_hit:
            b.destroy()

        for l in self.land.items:
            l.draw(self.win)

        for c in self.city.items:
            c.draw(self.win)

        for b in self.battery.items:
            b.draw(self.win)

        for m in self.missile.items:
            if m.active:
                m.draw(self.win)

        for b in self.bomb.items:
            if b.active:
                b.draw(self.win)

        for e in self.explosion.items:
            if e.active:
                e.state_machine.tick()
                if e.active:
                    e.draw(self.win)

        self.win.redraw()

        self.clock = self.clock + 1


game = Game()
game.load_level(1)

while True:
    game.tick()

    pnt = game.win.checkMouse()
    if not pnt is None:
        game.launch_missile(1, pnt.x, pnt.y, 5)
    time.sleep(0.1)

