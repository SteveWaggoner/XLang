#!/usr/bin/python3.9

from graphics import GraphWin, Point, Image, Rectangle, Circle, Line, Text
from c6502 import Byte, Word, WordDecimal

import bitmap
from playsound import playsound

from game_board import Game_UI
from game_objects import Object_Missile, Object_Bomb, Object_SmartBomb, Object_Plane, Object_Alien, Object_Mario, Object_Explosion, Object_City, Object_Battery, Object_Land

class Sound:

    def play(sound_name):
        if   sound_name == "load_level":       playsound("sounds/alert.mp3", False)
        elif sound_name == "launch_missile":   playsound("sounds/missile-fire.mp3", False)
        elif sound_name == "explode_enemy":    playsound("sounds/explosions.mp3", False)
        elif sound_name == "explode_friendly": playsound("sounds/city-blow-up.mp3", False)
        else: raise Exception("Unknown sound name: "+sound_name)



class Display:

    def __init__(self, clock):

        self.clock = clock
        self.window = bitmap.Window()
        self.graphic = []

    def draw(self, obj):

        if   isinstance(obj, Game_UI):          self.draw_ui(obj)
        elif isinstance(obj, Object_Missile):   self.draw_missile(obj)
        elif isinstance(obj, Object_Bomb):      self.draw_bomb(obj)
        elif isinstance(obj, Object_SmartBomb): self.draw_smartbomb(obj)
        elif isinstance(obj, Object_Plane):     self.draw_plane(obj)
        elif isinstance(obj, Object_Alien):     self.draw_alien(obj)
        elif isinstance(obj, Object_Mario):     self.draw_mario(obj)
        elif isinstance(obj, Object_Explosion): self.draw_explosion(obj)
        elif isinstance(obj, Object_Battery):   self.draw_battery(obj)
        elif isinstance(obj, Object_City):      self.draw_city(obj)
        elif isinstance(obj, Object_Land):      self.draw_land(obj)
        else: raise Exception(f"Unknown obj to draw: {type(obj)}")


    def draw_ui(self, ui):
        self.draw_text(Byte(60), Byte(20), str(ui.debug))
        self.draw_text(Byte(180), Byte(10), "level: "+str(ui.level)+"   score:" + str(ui.score))
        if ui.game_over == True:
            self.draw_text(Byte(180), Byte(100), "GAME OVER")


    def draw_missile(self, obj):
        self.draw_line(obj.start.x, obj.start.y, obj.pos.x, obj.pos.y)
        self.draw_circle(obj.pos.x, obj.pos.y, Byte(1))

    def draw_bomb(self, obj):
        self.draw_line(obj.start.x, obj.start.y, obj.pos.x, obj.pos.y)
        self.draw_circle(obj.pos.x, obj.pos.y, Byte(1))

    def draw_smartbomb(self, obj):
        self.draw_line(obj.pos.x-2, obj.pos.y-2, obj.pos.x+2, obj.pos.y+2)
        self.draw_line(obj.pos.x+2, obj.pos.y-2, obj.pos.x-2, obj.pos.y+2)
        self.draw_circle(obj.pos.x, obj.pos.y, Byte(1))

    def draw_plane(self, obj):
        self.draw_circle(obj.pos.x, obj.pos.y, obj.radius)

    def draw_alien(self, obj):
        self.draw_rectangle(obj.pos.x, obj.pos.y, obj.pos.x+obj.width, obj.pos.y+obj.height)

    def draw_mario(self, obj):
        self.draw_rectangle(obj.pos.x, obj.pos.y, obj.pos.x+obj.width, obj.pos.y+obj.height)
        self.window.background.img.fill_rect(int(obj.pos.x.get()), int(obj.pos.y.get()), int(obj.width.get()), int(obj.height.get()), "#F0D30F")

    def draw_explosion(self, obj):
        self.draw_circle(obj.pos.x, obj.pos.y, obj.radius)

    def draw_battery(self, obj):
        self.draw_rectangle(obj.pos.x, obj.pos.y, obj.pos.x+obj.width, obj.pos.y+obj.height)
        if obj.selected == True:
            self.draw_rectangle(obj.pos.x+2, obj.pos.y+2, obj.pos.x+obj.width-2, obj.pos.y+obj.height-2)
        self.draw_text(obj.pos.x + obj.width/2, obj.pos.y + obj.height/2, str(obj.num_missiles))

    def draw_city(self, obj):
        if obj.destroyed == True:
            self.draw_rectangle(obj.pos.x, obj.pos.y + (obj.height-1), obj.pos.x+obj.width, obj.pos.y+obj.height)
        else:
            self.draw_rectangle(obj.pos.x, obj.pos.y, obj.pos.x+obj.width, obj.pos.y+obj.height)

    def draw_land(self, obj):
        self.draw_rectangle(obj.pos.x, obj.pos.y, obj.pos.x+obj.width, obj.pos.y+obj.height)


    # helper routines
    def draw_line(self, x1,y1, x2,y2):
        self.graphic.append(Line(Point(x1.get(),y1.get()), Point(x2.get(), y2.get())))

    def draw_circle(self, x, y, radius):
        self.graphic.append(Circle(Point(x.get(), y.get()), radius.get()))

    def draw_rectangle(self, x1, y1, x2, y2):
        self.graphic.append(Rectangle(Point(x1.get(), y1.get()), Point(x2.get(), y2.get())))

    def draw_text(self, x, y, text):
        self.graphic.append(Text(Point(x.get(), y.get()), text))

    def start_draw(self):
        for g in self.graphic:
            g.undraw()
        self.graphic = []

        if self.clock.ticks % 8 == 0:
            self.window.draw_background()


    def finish_draw(self):
        for g in self.graphic:
            g.draw(self.window.win)
        self.window.flush()


    def check_key(self):
        return self.window.checkKey()

    def check_mouse(self):
        print(self.window)
        return self.window.checkMouse()

