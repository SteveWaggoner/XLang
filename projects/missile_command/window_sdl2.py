#!/usr/bin/python3.9

import sys
from sdl2 import *
import ctypes

class MouseClick:
    def __init__(self,x,y,button):
        self.x = x
        self.y = y
        self.button = button

class Window:
    def __init__(self, mode="VGA"):
        self.set_mode(mode)

        self.last_key = None
        self.last_mouse = None

    def set_mode(self,mode):

        if mode == "VGA":
            bkcolor = "#DFDFDF" #white
            width   = 320
            height  = 200
            scale_x = 4
            scale_y = 4
        elif mode == "C64_MC":
            bkcolor = "#FFFFFF" #white
            width   = 160
            height  = 200
            scale_x = 8
            scale_y = 4
        else:
            raise Exception(f"Unknown mode: {mode}")

        self.scale_x = scale_x
        self.scale_y = scale_y


        SDL_Init(SDL_INIT_EVERYTHING)
        self.window   = SDL_CreateWindow(b"SDL2 Window", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 960, 720, SDL_WINDOW_SHOWN)
        self.renderer = SDL_CreateRenderer(self.window, -1, 0)
        self.surface  = SDL_CreateRGBSurface(SDL_SWSURFACE, 160, 100, 32, 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000)

        self.event    = SDL_Event()



    def start_draw(self):
        print("start_draw")
        # clear surface
        SDL_FillRect(self.surface, None, 0)

        self.set_color(0xfffff08f)
        print("done start_Draw")

    def finish_draw(self):
        print("finish_draw")
        texture = SDL_CreateTextureFromSurface(self.renderer, self.surface)
        SDL_RenderCopy(self.renderer, texture, None, None)
        SDL_RenderPresent(self.renderer)

        self.poll_events()

    def poll_events(self):
        if SDL_PollEvent(ctypes.byref(self.event)) != 0:
            if self.event.type == SDL_QUIT:
                sys.exit(0)

            elif self.event.type == SDL_MOUSEBUTTONDOWN:

                mouseX = ctypes.c_int(0)
                mouseY = ctypes.c_int(0)
                SDL_GetMouseState(ctypes.byref(mouseX), ctypes.byref(mouseY))

                print(mouseX)
                self.last_mouse = MouseClick(mouseX.value, mouseY.value, self.event.button.button)

            elif self.event.type == SDL_KEYDOWN:
                self.last_key = event.key.keysym.sym


    def check_key(self):
        ret_key = self.last_key
        self.last_key = None
        return ret_key

    def check_mouse(self):
        ret_mouse = self.last_mouse
        self.last_mouse = None
        return ret_mouse


    def set_color(self, color):
        # get pointer to pixels as uint32[]
        u32_pixels = ctypes.cast(self.surface[0].pixels, ctypes.POINTER(ctypes.c_uint32))
        # get surface width
        width  = self.surface[0].w
        height = self.surface[0].h
        color  = 0xfffff08f
        self.put_pixel = lambda x,y: draw_pixel(u32_pixels, width, height, x, y, color)



    def draw_line(self, x1,y1, x2,y2):
        line(int(x1.get()),int(y1.get()),int(x2.get()),int(y2.get()), self.put_pixel)

    def draw_circle(self, x, y, radius):
        circle(int(x.get()),int(y.get()),int(radius.get()), self.put_pixel)

    def draw_rectangle(self, x1, y1, x2, y2):
        self.draw_line(x1,y1,x1,y2)
        self.draw_line(x1,y1,x2,y1)
        self.draw_line(x2,y1,x2,y2)
        self.draw_line(x1,y2,x2,y2)

    def draw_text(self, x, y, text):
        pass




def draw_pixel(pixels,width,height, x,y, color32):
    print("draw_pixel")
    if x>=0 and y>=0 and x<width and y<height:
        print(pixels)
        print(f"width={width}, height={height}")
        print(f"x={x},y={y}")
        pixels[y*width + x] = color32
    else:
        pass #off screen
    print("done draw_pixel")




def circle(x0, y0, radius, putPixel):
    f = 1 - radius
    ddf_x = 1
    ddf_y = -2 * radius
    x = 0
    y = radius
    putPixel(x0, y0 + radius)
    putPixel(x0, y0 - radius)
    putPixel(x0 + radius, y0)
    putPixel(x0 - radius, y0)

    while x < y:
        if f >= 0:
            y -= 1
            ddf_y += 2
            f += ddf_y
        x += 1
        ddf_x += 2
        f += ddf_x
        putPixel(x0 + x, y0 + y)
        putPixel(x0 - x, y0 + y)
        putPixel(x0 + x, y0 - y)
        putPixel(x0 - x, y0 - y)
        putPixel(x0 + y, y0 + x)
        putPixel(x0 - y, y0 + x)
        putPixel(x0 + y, y0 - x)
        putPixel(x0 - y, y0 - x)

        print(x)


def line(x0, y0, x1, y1, putPixel):
    """Yields the points of a line between (x0, y0) and (x1, y1) using Bresenham's algorithm."""

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    err = dx - dy

    while True:
        putPixel (x, y)
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy


