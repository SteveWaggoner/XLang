#!/usr/bin/python3.9

from c6502 import Byte, Word, WordDecimal, DWord
from game_objects import *
from list import List
from game_levels import Game_Levels

import random
random.seed(123) # make game deterministic

class Game_Board:

    def __init__(self):

        self.clock            = Clock()

        self.level_index      = Byte(0)
        self.enemy_index      = Byte(0)

        self.level            = None

        self.game_over        = Byte(False)
        self.level_over       = Byte(False)
        self.score            = DWord(0)
        self.next_city_score  = DWord(10000)
        self.extra_cities     = Byte(0)

        self.switching_to_next_level = Byte(False)

        self.create_game_objects()
        self.create_event_handlers()


    def create_game_objects(self):

        self.missile   = List(Object_Missile,15)
        self.bomb      = List(Object_Bomb,25)
        self.smartbomb = List(Object_SmartBomb,4)
        self.mario     = List(Object_Mario,4)
        self.plane     = List(Object_Plane,4)
        self.alien     = List(Object_Alien,4)
        self.explosion = List(Object_Explosion,15)

        self.city = List(Object_City, 6, True)
        self.city[0].set_position(Position(x =  46, y=180), width=20,height=5)
        self.city[1].set_position(Position(x =  78, y=180), width=20,height=5)
        self.city[2].set_position(Position(x = 108, y=180), width=20,height=5)
        self.city[3].set_position(Position(x = 172, y=180), width=20,height=5)
        self.city[4].set_position(Position(x = 210, y=180), width=20,height=5)
        self.city[5].set_position(Position(x = 246, y=180), width=20,height=5)

        self.battery = List(Object_Battery, 3, True)
        self.battery[0].set_position(Position(x= 12,y=176), width=28,height=10)
        self.battery[1].set_position(Position(x=140,y=176), width=28,height=10)
        self.battery[2].set_position(Position(x=280,y=176), width=28,height=10)
        self.battery_index = Byte(1)

        self.land = List(Object_Land, 1, True)
        self.land[0].set_position(Position(x=0, y=185),width=320, height=15)

    def create_event_handlers(self):
        self.on_load_level     = None
        self.on_launch_missile = None
        self.on_explode_enemy  = None


    def load_level(self, level_index):

        level_index = level_index % len(Game_Levels.levels)

        self.clock.reset()

        self.level_index.set(level_index)
        self.level = Game_Levels.levels[level_index]
        self.enemy_index.set(0)

        if self.on_load_level:
            self.on_load_level()

        for game_objs in [self.missile, self.bomb]:
            game_objs.clear()

        for battery in self.battery.items:
            battery.num_missiles.set(10)

    def spawn_enemies(self):

        if self.enemy_index < len(self.level.enemy):
            enemy = self.level.enemy[self.enemy_index.get()]
            if enemy.launch_time < self.clock.ticks:
                enemy.spawn(self)
                self.enemy_index += 1


    def any_active(game_objs_array):
        for game_objs in game_objs_array:
            if game_objs.num_active > 0:
                return True
        return False

    def get_random(game_objs_array):
        active_items = []
        for game_objs in game_objs_array:
            if game_objs.num_active > 0:
                for game_obj in game_objs.items:
                    if game_obj.active == True:
                        active_items.append(game_obj)
        return random.choice(active_items)


    def get_random_target(self):
        game_obj = Game_Board.get_random([self.battery, self.city])
        return game_obj.get_target_pos()

    def select_battery(self, battery_index):
        self.battery_index.set(battery_index)


    def launch_missile(self, dest_x, dest_y, speed):

        battery = self.battery[self.battery_index.get()]

        if dest_y > battery.pos.y:
            return False

        if battery.num_missiles < 1:
            return False

        if self.on_launch_missile:
            self.on_launch_missile()

        missile = self.missile.create()
        start_x = battery.pos.x + (battery.width/2)
        start_y = battery.pos.y
        missile.set_position(Position(start_x,start_y),Position(dest_x,dest_y), speed)

        battery.num_missiles = battery.num_missiles - 1
        return True


    def create_explosion(self, pos):

        e = self.explosion.create()
        e.set_position(pos)


    def create_attack(self, plane, attack_type):

        print("create_attack")

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
        print("score level")
        for battery in self.battery.items:
            self.score = self.score + (5 * battery.num_missiles.get()) # 5 points per unused missile

        for city in self.city.items:
            if not city.destroyed.get():
                self.score = self.score + (200)  # 100 points per saved city

        while self.score.get() >= self.next_city_score.get():
            self.extra_cities += 1
            self.next_city_score += 10000



    def dodge_nearby_explosions(self, enemy):
        for explosion in self.explosion.items:
            if explosion.active == True:
                if explosion.pos.distance_to(enemy.pos) < 90 and enemy.last_dodge + 5 < self.clock.ticks:
                    enemy.last_dodge = self.clock.ticks
                    if enemy.route:
                        enemy.route.insert(enemy.route_index.get(), enemy.dest)
                    else:
                        enemy.route = [enemy.dest]
                    enemy.dest = Position(enemy.pos.x + (enemy.velocity.x * 6), enemy.pos.y - (enemy.velocity.y * 8))
                    enemy.update_vectors()
                    break


    def move_items(self, collection, enable_attack=False, enable_explode=False, enable_dodge=False):

        for item in collection.items:
            if item.active == True:
                item.move()

                if enable_attack and item.attack_times:
                    if self.clock.ticks in item.attack_times:
                        attack_n = item.attack_times.index(self.clock.ticks)
                        attack_type = item.attack_types[attack_n % len(item.attack_types)]
                        self.create_attack(item, attack_type)


                at_dest = item.distance < 50 and \
                            item.last_distance is not None and item.distance > item.last_distance # actually past destination
                if at_dest:

                    if item.route and item.route_index < len(item.route):
                        next_dest = item.route[item.route_index.get()]
                        item.route_index += 1
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


    def move_game_objects(self):
        self.move_items(self.bomb)
        self.move_items(self.smartbomb, enable_dodge=True)
        self.move_items(self.plane, enable_attack=True)
        self.move_items(self.alien, enable_attack=True)
        self.move_items(self.missile, enable_explode=True)
        self.move_items(self.mario, enable_explode=False)


    def explode_enemies(self):

        self.explode_enemy(self.bomb, 25)
        self.explode_enemy(self.plane, 100)
        self.explode_enemy(self.alien, 100)
        self.explode_enemy(self.smartbomb, 125)
        self.explode_enemy(self.mario, 125)


    def explode_friendly(self, friendly):

        for enemy in [self.bomb, self.smartbomb, self.mario]:
            if enemy.num_active > 0:
                hits = enemy.get_collisions(friendly, Object.collide_pnt_in_rect)
                for hit_enemy, hit_friendly in hits:
                    hit_enemy.destroy()
                    hit_friendly.destroy()
                    if self.on_explode_friendly:
                        self.on_explode_friendly()


    def explode_friendlies(self):

        self.explode_friendly(self.city)
        self.explode_friendly(self.battery)
        self.explode_friendly(self.land)



    def explode_enemy(self, enemy, score_points):
        bombs_hit = self.explosion.get_collisions(enemy, Object.collide_circles)
        for explosion, enemy in bombs_hit:
            self.score += score_points
            enemy.destroy()
            if self.on_explode_enemy:
                self.on_explode_enemy()

    def has_more_enemies_to_launch(self):
        return self.level.enemy[-1].launch_time > self.clock.ticks

    def has_more_enemies_in_flight(self):
        return Game_Board.any_active([self.missile,self.explosion,self.bomb,self.plane,self.alien,self.smartbomb])

    def has_clock_alarms(self):
        return Game_Board.any_active([self.clock.alarms])

    def is_level_active(self):
        return self.has_more_enemies_to_launch() or self.has_more_enemies_in_flight()

    def check_if_level_over(self):

        if self.game_over == False:

            level_over = not self.is_level_active()
            if level_over and self.switching_to_next_level == False:
                print("switching level...")
                self.clock.set_alarm(2, self.score_level)
                self.clock.set_alarm(4, self.next_level)
                self.switching_to_next_level.set(True)

    def check_if_game_over(self):

        valid_cities = 0
        for city in self.city.items:
            if not city.destroyed.get():
                valid_cities = valid_cities + 1

        if valid_cities == 0:
            self.game_over.set(True)

    def is_game_active(self):
        return self.game_over == False or self.is_level_active()


    def next_level(self):

        print("next level")
        self.load_level(self.level_index.get() + 1)
        self.switching_to_next_level.set(False)


    def game_action(self):

        self.check_if_level_over()
        self.check_if_game_over()

        self.spawn_enemies()
        self.move_game_objects()
        self.explode_enemies()
        self.explode_friendlies()

        self.clock.tick()
        self.clock.check_alarms()




def main():
    print("start game")

    board = Game_Board()
    board.load_level(0)
    while board.is_game_active():
        board.game_action()

    print("end game")



if __name__=="__main__":
    main()


