#!/usr/bin/python3.9

import sys
from sdl2 import *
from sdl2.sdlttf import *
import ctypes

import geometry

from list import Item, List

class Transform:

    """Internal class for 2-D coordinate transformations"""

    def __init__(self, w, h, xlow, ylow, xhigh, yhigh):
        # w, h are width and height of window
        # (xlow,ylow) coordinates of lower-left [raw (0,h-1)]
        # (xhigh,yhigh) coordinates of upper-right [raw (w-1,0)]
        xspan = (xhigh-xlow)
        yspan = (yhigh-ylow)
        self.xbase = xlow
        self.ybase = yhigh
        self.xscale = xspan/float(w-1)
        self.yscale = yspan/float(h-1)


    def to_int(n):
        if isinstance(n, int) or isinstance(n,float):
            return int(n)
        else:
            return int(n.get())


    def to_screen(self,x,y):
        x = Transform.to_int(x)
        y = Transform.to_int(y)

        # Returns x,y in screen (actually window) coordinates
        xs = (x-self.xbase) / self.xscale
        ys = (self.ybase-y) / self.yscale
        return int(xs+0.5),int(ys+0.5)

    def to_world(self,xs,ys):
        # Returns xs,ys in world coordinates
        x = xs*self.xscale + self.xbase
        y = self.ybase - ys*self.yscale
        return x,y


class MouseClick:
    def __init__(self,x,y,button):
        self.x = x
        self.y = y
        self.button = button
    def __repr__(self):
        return f"x={self.x}, y={self.y}, button={self.button}"



class Canvas:
    def __init__(self, surface, bkgnd_surface=None, transform=None):
        self.surface = surface
        self.bkgnd_surface = bkgnd_surface

        if transform is None:
            # no transform
            transform = Transform(surface[0].w, surface[0].h, 0,0, surface[0].w, surface[0].h)

        self.transform = transform
        self.font = None
        self.set_color(0xfffff08f)

        # get pointer to pixels as uint32[]
        self.pixels = ctypes.cast(self.surface[0].pixels, ctypes.POINTER(ctypes.c_uint32))
        # get surface width
        self.width  = self.surface[0].w
        self.height = self.surface[0].h

        if bkgnd_surface:
            self.bkgnd_pixels = ctypes.cast(self.bkgnd_surface[0].pixels, ctypes.POINTER(ctypes.c_uint32))
            self.bkgnd_width  = self.bkgnd_surface[0].w
            self.bkgnd_height = self.bkgnd_surface[0].h
        else:
            self.bkgnd_width  = 0
            self.bkgnd_height = 0

        self.erase_list = []


    def _put_pixel(self, x,y,color32,mode):
        if mode == "normal":
            self._write_pixel(x,y,color32)
        elif mode == "xor":
            old_color = self._read_pixel(x,y)
            if old_color is not None:
                new_color = (old_color ^ color32) | 0xFF000000
                self._write_pixel(x,y, new_color)
            else:
                print(f"cannot read old color at {x},{y}")

        elif mode == "erase":
            bkgnd_color = self._read_bkgnd_pixel(x,y)
            if bkgnd_color is not None:
                self._write_pixel(x,y, bkgnd_color)
        else:
            raise Exception(f"unknown draw pixel mode: {mode}")




    def _read_pixel(self,x,y):
        if x>=0 and y>=0 and x<self.width and y<self.height:
            return self.pixels[y*self.width + x]

    def _read_bkgnd_pixel(self,x,y):
        if x>=0 and y>=0 and x<self.bkgnd_width and y<self.bkgnd_height:
            return self.bkgnd_pixels[y*self.bkgnd_width + x]

    def _write_pixel(self,x,y, color32):
        if x>=0 and y>=0 and x<self.width and y<self.height:
            self.pixels[y*self.width + x] = color32

    def _write_bkgnd_pixel(self,x,y, color32):
        if x>=0 and y>=0 and x<self.bkgnd_width and y<self.bkgnd_height:
            self.bkgnd_pixels[y*self.bkgnd_width + x] = color32


    def _clear_bkgnd(self, rect, color32):
        ret = SDL_FillRect(self.bkgnd_surface, None, color32)



    def set_color(self, color, mode="normal", erase_later=False):
        if color is None:
            raise Exception("color is null?!?")

        self.color = color
        self.erase_later = erase_later
        self.put_pixel = lambda x,y: self._put_pixel(x, y, color, mode)
        self.erase_pixel = lambda x,y: self._put_pixel(x, y, None, "erase")


    def erase(self):
        for erase in self.erase_list:
            erase()
        self.erase_list = []


    def clear(self):
        self._filled_rect(None, 0xFF000000) #black with 100% alpha (no transparency)

    def _filled_rect(self, rect, color):
        ret = SDL_FillRect(self.surface, rect, color)


    def draw_pixel(self, x, y):
        sx,sy = self.transform.to_screen(x,y)
        self.put_pixel(sx,sy)
        if self.erase_later:
            self.erase_list.append(lambda : self.erase_pixel(sx,sy))


    def draw_line(self, x1,y1, x2,y2):

        sx1,sy1 = self.transform.to_screen(x1,y1)
        sx2,sy2 = self.transform.to_screen(x2,y2)

        geometry.Shape.line(sx1,sy1,sx2,sy2, self.put_pixel)
        if self.erase_later:
            self.erase_list.append(lambda : geometry.Shape.line(sx1,sy1,sx2,sy2, self.erase_pixel))


    def draw_filled_circle(self,x,y,radius):
        sx,sy = self.transform.to_screen(x,y)
        radius = Transform.to_int(radius)
        geometry.Shape.filled_circle(sx,sy,radius, self.put_pixel)
        if self.erase_later:
            self.erase_list.append(lambda : geometry.Shape.filled_circle(sx,sy,radius, self.erase_pixel))

    def draw_filled_octogon(self,x,y,radius, slope_dx, slope_dy):
        sx,sy = self.transform.to_screen(x,y)
        radius = Transform.to_int(radius)
        geometry.Shape.filled_octogon(sx,sy,radius, slope_dx, slope_dy, self.put_pixel)
        if self.erase_later:
            self.erase_list.append(lambda : geometry.Shape.filled_octogon(sx,sy,radius, 3,8, self.erase_pixel))


    def draw_circle(self, x, y, radius):
        sx,sy = self.transform.to_screen(x,y)
        radius = Transform.to_int(radius)
        geometry.Shape.circle(sx,sy,radius, self.put_pixel)
        if self.erase_later:
            self.erase_list.append(lambda : geometry.Shape.circle(sx,sy,radius, self.erase_pixel))

    def draw_rectangle(self, x1, y1, x2, y2):
        self.draw_line(x1,y1,x1,y2)
        self.draw_line(x1,y1,x2,y1)
        self.draw_line(x2,y1,x2,y2)
        self.draw_line(x1,y2,x2,y2)

    def draw_text(self, x, y, text):

        if not self.font:
            self.font = TTF_OpenFont(b"fonts/ARCADE_R.TTF", 8)
            if not self.font:
                raise Exception(f"TTF_OpenFont() error = {TTF_GetError()}")

        # Create surface with rendered text
        textColor  = pixels.SDL_Color(100, 110, 160)
        textSurface = TTF_RenderText_Solid(self.font, text.encode(), textColor);
        if not textSurface:
            print(f"Failed to create text surface: {TTF_GetError()}")


        sx,sy = self.transform.to_screen(x,y)
        rcDest = SDL_Rect()
        rcDest.x = sx
        rcDest.y = sy
        rcDest.w = textSurface[0].w
        rcDest.h = textSurface[0].h

        SDL_BlitSurface(textSurface, None, self.surface, ctypes.byref(rcDest))
        SDL_FreeSurface(textSurface)

        if self.erase_later:
            bkgnd_color = self._read_bkgnd_pixel(sx,sy)
            self.erase_list.append(lambda : self._filled_rect(rcDest, bkgnd_color))



    def draw_image(self, canvas, x=0, y=0):

        sx,sy = self.transform.to_screen(x,y)
        rcDest = SDL_Rect()
        rcDest.x = sx
        rcDest.y = sy
        rcDest.w = canvas.surface[0].w
        rcDest.h = canvas.surface[0].h

        SDL_BlitSurface(canvas.surface, None, self.surface, ctypes.byref(rcDest))

        if self.erase_later:
            bkgnd_color = self._read_pixel(sx,sy)
            self.erase_list.append(lambda : self._filled_rect(rcDest, bkgnd_color))






class Image:
    def __init__(self, width, height, centerx, centery):
        super().__init__()
        surface  = SDL_CreateRGBSurface(SDL_SWSURFACE, width, height, 32, 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000)
        self.canvas = Canvas(surface)
        self.centerx = centerx
        self.centery = centery


class Sprite(Item):
    def __init__(self):
        super().__init__()
        self.x = None
        self.y = None
        self.image = None

    def set(self,image, x,y):
        self.image = image
        self.x = x
        self.y = y




class Window:

    SDL_Init(SDL_INIT_EVERYTHING)
    TTF_Init()

    def __init__(self, title, mode="VGA"):

        if mode == "SVGA":
            width   = 800
            height  = 600
            self.scale_x = 1
            self.scale_y = 1
        elif mode == "VGA":
            width   = 320
            height  = 200
            self.scale_x = 4
            self.scale_y = 4
        elif mode == "C64_MC":
            width   = 160
            height  = 200
            self.scale_x = 8
            self.scale_y = 4
        else:
            raise Exception(f"Unknown mode: {mode}")


        self.window   = SDL_CreateWindow(title.encode(), SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, width*self.scale_x, height*self.scale_y, SDL_WINDOW_SHOWN)
        self.renderer = SDL_CreateRenderer(self.window, -1, 0)

        surface_fg     = SDL_CreateRGBSurface(SDL_SWSURFACE, width, height, 32, 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000)
        surface_bg     = SDL_CreateRGBSurface(SDL_SWSURFACE, width, height, 32, 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000)
        surface_merged = SDL_CreateRGBSurface(SDL_SWSURFACE, width, height, 32, 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000)
        transform = Transform(width, height,  0, 200, 320, 0)

        self.canvas = Canvas(surface_fg,surface_bg,transform=transform)
        self.canvas_merged = Canvas(surface_merged,transform=transform)

        self.texture  = None
        self.event    = SDL_Event()
        self.images   = {}

        self.last_mouse = None
        self.last_key   = None

        self.sprites = List(Sprite,20)


    def add_image(self, name, image):
        self.images[name] = image


    def start_draw(self):
      #  self.canvas.clear()
        self.canvas.erase()
        self.sprites.clear()

    def draw_sprite(self, name, x, y):
        sprite = self.sprites.create()
        sprite.set(self.images[name], x, y)
        # draw sprite in the finish_draw()

    def finish_draw(self):
        if self.texture != None:
            SDL_DestroyTexture(self.texture)

        self.canvas_merged.clear()
        self.canvas_merged.draw_image(self.canvas,0,0)
        for sprite in self.sprites:
            if sprite.active == True:
                self.canvas_merged.draw_image(sprite.image.canvas, sprite.x - sprite.image.centerx, sprite.y - sprite.image.centery)



        self.texture = SDL_CreateTextureFromSurface(self.renderer, self.canvas_merged.surface)
        SDL_RenderCopy(self.renderer, self.texture, None, None)
        SDL_RenderPresent(self.renderer)

        self.poll_events()

    def poll_events(self):
        while SDL_PollEvent(ctypes.byref(self.event)) != 0:
            if self.event.type == SDL_QUIT:
                sys.exit(0)

            elif self.event.type == SDL_MOUSEBUTTONDOWN:

                mouseX = ctypes.c_int(0)
                mouseY = ctypes.c_int(0)
                SDL_GetMouseState(ctypes.byref(mouseX), ctypes.byref(mouseY))
                wx, wy = self.canvas.transform.to_world(mouseX.value, mouseY.value)
                wx, wy = wx / self.scale_x, wy / self.scale_y #hack for stretched canvas
                self.last_mouse = MouseClick(wx, wy, self.event.button.button)

            elif self.event.type == SDL_KEYDOWN:
                self.last_key = self.event.key.keysym.sym


    def check_key(self):
        ret_key = self.last_key
        self.last_key = None
        return ret_key

    def check_mouse(self):
        ret_mouse = self.last_mouse
        self.last_mouse = None
        return ret_mouse


