#!/usr/bin/python3.9

from c6502 import Byte, Word, WordDecimal

#from playsound import playsound

from game_board import Game_UI
from game_objects import Object_Missile, Object_Bomb, Object_SmartBomb, Object_Plane, Object_Alien, Object_Mario, Object_Explosion, Object_City, Object_Battery, Object_Land


from window_sdl2 import Image

class Sound:

    def play(sound_name):
        if   sound_name == "load_level":       playsound("sounds/alert.mp3", False)
        elif sound_name == "launch_missile":   playsound("sounds/missile-fire.mp3", False)
        elif sound_name == "explode_enemy":    playsound("sounds/explosions.mp3", False)
        elif sound_name == "explode_friendly": playsound("sounds/city-blow-up.mp3", False)
        else: raise Exception("Unknown sound name: "+sound_name)

# format is reverse HTML hex!! AGBR
class Color:
#    RED=0xFFFF1707        #red plane, red missile
    RED=0xFF0717FF        #red plane, red missile
    LIGHT_RED=0xFF0001FD  #light part of plane
    YELLOW=0xFF00F1FF     #yellow explosion
    BLACK=0xFF000000      #black background

    DARK_BLUE=0xFFAD0000  #dark part of alien eye
    BLUE=0xFFD50C05       #blue crosshairs, blue missiles
    LIGHT_BLUE=0xFFFFDF09 #light blue in cities (mixed with blue)

    ORANGE=0xFF00A6FF     #tips of alien antenna

    GREEN=0xFF51E852     #green explosions, green land (yellow background)
    LAVENDER=0xFFF303E8  #different level?

    TRANSPARENT=0x00000000 #transparent


class Asset:

    def __init__(self, width, height, colors, pixel_str, flip=False):
        pixels = []
        centerx = 0
        centery = 0

        for line in pixel_str.splitlines():
            if flip:
                line = line[::-1] # reverse string
            for ch in line.strip():
                if ch == "X":
                    centerx = len(pixels) % width
                    centery = len(pixels) // width
                pixels.append(colors[ch])
        if len(pixels) != width*height:
            raise Exception(f"expecting {width*height} pixels but got {len(pixels)}")

        self.image = Image(width,height,centerx,centery)
        for i, c in enumerate(pixels):
            self.image.canvas.pixels[i] = c



plane_right = Asset(18,11,
              {".":Color.TRANSPARENT,
               "B":Color.BLACK,
               "R":Color.RED,
               "X":Color.RED,
               "r":Color.LIGHT_RED},
              """
              ....BRr...........
              .Br..BRr..........
              .BRr.BRRr.........
              .BRRRRRRRRRRRr....
              BRRRRRRRXRRRRRRr..
              ...BRRRRRRRRRRRRRr
              ....BRRRRr........
              ....BRRRr.........
              ...BRRRr..........
              ...BRRr...........
              ..BRRr............

              """)


plane_left = Asset(18,11,
              {".":Color.TRANSPARENT,
               "B":Color.BLACK,
               "R":Color.RED,
               "X":Color.RED,
               "r":Color.LIGHT_RED},
              """
              ....BRr...........
              .Br..BRr..........
              .BRr.BRRr.........
              .BRRRRRRRRRRRr....
              BRRRRRRRXRRRRRRr..
              ...BRRRRRRRRRRRRRr
              ....BRRRRr........
              ....BRRRr.........
              ...BRRRr..........
              ...BRRr...........
              ..BRRr............

              """,
              flip=True)


alien = Asset(14,13,
              {".":Color.TRANSPARENT,
               "B":Color.BLACK,
               "R":Color.RED,
               "r":Color.LIGHT_RED,
               "X":Color.LIGHT_RED,
               "O":Color.ORANGE,
               "D":Color.DARK_BLUE,
               "b":Color.BLUE},
              """
              BO..........BO
              .Br........Br.
              ..Br.BRRr.Br..
              ...BRRRRRRr...
              ...BRRRRRRr...
              ..BrDbRrDbRr..
              ..BrDbRXDbRr..
              ..BrDbRrDbRr..
              ...BRRRRRRr...
              ...BRRRRRRr...
              ..Br.BRRr.Br..
              .Br........Br.
              BO..........BO
              """)

class Display:

    def __init__(self, window):
        self.window = window
        self.add_assets()

        self.erase_list = []

        self.sky_color   = Color.BLACK
        self.land_color  = Color.YELLOW

        self.enemy_color = Color.RED
        self.friendly_color = Color.BLUE

        self.city_color = Color.LIGHT_BLUE

        self.alien_color1 = Color.RED



    def add_assets(self):

        self.window.add_image("plane_left",  plane_left.image)
        self.window.add_image("plane_right", plane_right.image)
        self.window.add_image("alien", alien.image)


        img = Image(5,5,2,2)
        img.canvas.draw_line(0,0,5,5)
        img.canvas.draw_line(0,5,0,5)
        img.canvas.draw_circle(2,2,2)
        self.window.add_image("circle_cross_5_5", img)

        img = Image(8,8,4,4)
        img.canvas.draw_circle(4,4,3)
        self.window.add_image("tiny_circle",img)

        img = Image(40,40, 20,20)
        img.canvas.draw_filled_circle(20,20,18)
        self.window.add_image("big_circle",img)


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

        self.window.canvas.set_color(0xFF053499,erase_later=True)
        self.window.canvas.draw_text(Byte(60), Byte(20), str(ui.debug))
        self.window.canvas.draw_text(Byte(180), Byte(10), "level: "+str(ui.level)+"   score:" + str(ui.score))
        if ui.game_over == True:
            self.window.canvas.draw_text(Byte(180), Byte(100), "GAME OVER")


    def draw_missile(self, obj):

        self.window.canvas.set_color(0xFF053499, erase_later=True)
        self.window.canvas.draw_pixel(obj.pos.x, obj.pos.y)

    def draw_bomb(self, obj):
        self.window.draw_sprite("tiny_circle", obj.pos.x, obj.pos.y)

    def draw_smartbomb(self, obj):
        self.window.draw_sprite("circle_cross_5_5", obj.pos.x, obj.pos.y)

    def draw_plane(self, obj):

        if obj.velocity.x < 0:
            self.window.draw_sprite("plane_left", obj.pos.x, obj.pos.y)
        else:
            self.window.draw_sprite("plane_right", obj.pos.x, obj.pos.y)


    def draw_alien(self, obj):
        self.window.draw_sprite("alien", obj.pos.x, obj.pos.y)

    def draw_mario(self, obj):
        self.window.draw_sprite("tiny_circle", obj.pos.x, obj.pos.y)

    def draw_explosion(self, obj):
        self.window.canvas.set_color(0xFF153489, mode="xor", erase_later=True)
        self.window.canvas.draw_filled_octogon(obj.pos.x, obj.pos.y, obj.radius, 3,8)
        self.window.canvas.set_color(0xFF053499, mode="normal", erase_later=True)


    def draw_battery(self, obj):
        self.window.canvas.draw_rectangle(obj.pos.x, obj.pos.y, obj.pos.x+obj.width, obj.pos.y+obj.height)
        if obj.selected == True:
            self.window.canvas.draw_rectangle(obj.pos.x+2, obj.pos.y+2, obj.pos.x+obj.width-2, obj.pos.y+obj.height-2)
        self.window.canvas.draw_text(obj.pos.x + obj.width/2, obj.pos.y + obj.height/2, str(obj.num_missiles))

    def draw_city(self, obj):
        if obj.destroyed == True:
            self.window.canvas.draw_rectangle(obj.pos.x, obj.pos.y + (obj.height-1), obj.pos.x+obj.width, obj.pos.y+obj.height)
        else:
            self.window.canvas.draw_rectangle(obj.pos.x, obj.pos.y, obj.pos.x+obj.width, obj.pos.y+obj.height)

    def draw_land(self, obj):
        self.window.canvas.draw_rectangle(obj.pos.x, obj.pos.y, obj.pos.x+obj.width, obj.pos.y+obj.height)


    def start_draw(self):
        self.window.start_draw()


    def finish_draw(self):
        self.window.finish_draw()

    def check_key(self):
        return self.window.check_key()

    def check_mouse(self):
        return self.window.check_mouse()

