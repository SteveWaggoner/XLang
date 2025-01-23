#!/usr/bin/python3.9

from object import Position
from game_objects import Enemy

class Level:

    def __init__(self):
        self.enemy = []
        self.score_multiplier = 1
        self.backgroud_color = ""


class Game_Levels:

    levels = []
    levels.append(Level())
    levels[0].score_multiplier = 1
    levels[0].background_color = "blue"

    levels[0].enemy.append(Enemy("mario",launch_time=0.5,start=Position(x=180,y=0), speed=25, dest=Position(x=255, y=180)))

    levels[0].enemy.append(Enemy("smartbomb",launch_time=0.8,start=Position(x=180,y=0), speed=25, dest=Position(x=255, y=180)))

    levels[0].enemy.append(Enemy("alien",launch_time=3,start=Position(x=0,y=110), speed=25,
                           attack_times=[5,10],attack_types=["single_bomb"],
                           route=[Position(x=50, y=90),Position(x=100, y=50),Position(x=150, y=90),Position(x=320, y=50)]))

    levels[0].enemy.append(Enemy("plane",launch_time=4,start=Position(x=320,y=90), dest=Position(x=0, y=90), speed=25,
                           attack_times=[3,3.1,3.2,9,9.1,9.2,12,12.1],attack_types=["single_bomb","multiple_bombs"]))

    levels[0].enemy.append(Enemy("plane",launch_time=5,start=Position(x=320,y=90), dest=Position(x=0, y=90), speed=25,
                           attack_times=[3,3.1,32,90,91,92,120,121],attack_types=["single_bomb","multiple_bombs"]))


    levels.append(Level())
    levels[1].enemy.append(Enemy("mario",launch_time=0.5,start=Position(x=180,y=0), speed=25, dest=Position(x=255, y=180)))

    levels[1].enemy.append(Enemy("smartbomb",launch_time=0.8,start=Position(x=180,y=0), speed=25, dest=Position(x=255, y=180)))

    levels[1].enemy.append(Enemy("alien",launch_time=3,start=Position(x=0,y=110), speed=25,
                           attack_times=[5,10],attack_types=["single_bomb"],
                           route=[Position(x=50, y=90),Position(x=100, y=50),Position(x=150, y=90),Position(x=320, y=50)]))

    levels[1].enemy.append(Enemy("plane",launch_time=4,start=Position(x=320,y=90), dest=Position(x=0, y=90), speed=25,
                           attack_times=[3,3.1,3.2,9,9.1,9.2,12,12.1],attack_types=["single_bomb","multiple_bombs"]))

    levels[1].enemy.append(Enemy("plane",launch_time=5,start=Position(x=320,y=90), dest=Position(x=0, y=90), speed=25,
                           attack_times=[3,3.1,32,90,91,92,120,121],attack_types=["single_bomb","multiple_bombs"]))



    levels.append(Level())
    levels[2].enemy.append(Enemy("mario",launch_time=0.5,start=Position(x=180,y=0), speed=25, dest=Position(x=255, y=180)))

    levels[2].enemy.append(Enemy("smartbomb",launch_time=0.8,start=Position(x=180,y=0), speed=25, dest=Position(x=255, y=180)))

    levels[2].enemy.append(Enemy("alien",launch_time=3,start=Position(x=0,y=110), speed=25,
                           attack_times=[5,10],attack_types=["single_bomb"],
                           route=[Position(x=50, y=90),Position(x=100, y=50),Position(x=150, y=90),Position(x=320, y=50)]))

    levels[2].enemy.append(Enemy("plane",launch_time=4,start=Position(x=320,y=90), dest=Position(x=0, y=90), speed=25,
                           attack_times=[3,3.1,3.2,9,9.1,9.2,12,12.1],attack_types=["single_bomb","multiple_bombs"]))

    levels[2].enemy.append(Enemy("plane",launch_time=5,start=Position(x=320,y=90), dest=Position(x=0, y=90), speed=25,
                           attack_times=[3,3.1,32,90,91,92,120,121],attack_types=["single_bomb","multiple_bombs"]))




    levels.append(Level())
    levels[3].enemy.append(Enemy("bomb",launch_time=1,start=Position(x=10,y=0), dest=Position(x=55, y=200), speed=15))
    levels[3].enemy.append(Enemy("bomb",launch_time=5,start=Position(x=50,y=0), dest=Position(x=150, y=200), speed=15))
    levels[3].enemy.append(Enemy("bomb",launch_time=6,start=Position(x=70,y=0), dest=Position(x=230, y=200), speed=15))
    levels[3].enemy.append(Enemy("bomb",launch_time=8,start=Position(x=210,y=0), dest=Position(x=255, y=180), speed=15))


    levels.append(Level())
    levels[4].enemy.append(Enemy("bomb",launch_time=1,start=Position(x=10,y=0), dest=Position(x=55, y=200), speed=25))
    levels[4].enemy.append(Enemy("bomb",launch_time=3,start=Position(x=50,y=0), dest=Position(x=150, y=200), speed=25))
    levels[4].enemy.append(Enemy("bomb",launch_time=3,start=Position(x=270,y=0), dest=Position(x=180,y=200), speed=25))
    levels[4].enemy.append(Enemy("bomb",launch_time=3,start=Position(x=210,y=0), dest=Position(x=115,y=180), speed=25))
    levels[4].enemy.append(Enemy("bomb",launch_time=4,start=Position(x=110,y=0), dest=Position(x=115,y=180), speed=25))
    levels[4].enemy.append(Enemy("bomb",launch_time=3,start=Position(x=210,y=0), dest=Position(x=255,y=180), speed=25))
    levels[4].enemy.append(Enemy("bomb",launch_time=4,start=Position(x=110,y=0), dest=Position(x=85,y=180), speed=25))

    levels.append(Level())
    levels[5].enemy.append(Enemy("bomb",launch_time=1,start=Position(x=10,y=0), dest=Position(x=55, y=200), speed=15))
    levels[5].enemy.append(Enemy("bomb",launch_time=3,start=Position(x=15,y=0), dest=Position(x=55, y=200), speed=15))
    levels[5].enemy.append(Enemy("bomb",launch_time=3,start=Position(x=18,y=0), dest=Position(x=55, y=200), speed=15))
    levels[5].enemy.append(Enemy("bomb",launch_time=5,start=Position(x=50,y=0), dest=Position(x=150, y=200), speed=15))
    levels[5].enemy.append(Enemy("bomb",launch_time=5,start=Position(x=54,y=0), dest=Position(x=150, y=200), speed=15))
    levels[5].enemy.append(Enemy("bomb",launch_time=5,start=Position(x=58,y=0), dest=Position(x=150, y=200), speed=15))
    levels[5].enemy.append(Enemy("bomb",launch_time=6,start=Position(x=70,y=0), dest=Position(x=230, y=200), speed=15))
    levels[5].enemy.append(Enemy("bomb",launch_time=6,start=Position(x=72,y=0), dest=Position(x=230, y=200), speed=15))
    levels[5].enemy.append(Enemy("bomb",launch_time=6,start=Position(x=73,y=0), dest=Position(x=230, y=200), speed=15))
    levels[5].enemy.append(Enemy("bomb",launch_time=8,start=Position(x=210,y=0), dest=Position(x=255, y=180), speed=15))
    levels[5].enemy.append(Enemy("bomb",launch_time=8,start=Position(x=211,y=0), dest=Position(x=255, y=180), speed=15))
    levels[5].enemy.append(Enemy("bomb",launch_time=8,start=Position(x=218,y=0), dest=Position(x=255, y=180), speed=15))


