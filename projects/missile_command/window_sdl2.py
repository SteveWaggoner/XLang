#!/usr/bin/python3.9

import sys
from sdl2 import *
from sdl2.sdlttf import *
import ctypes

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
    def __init__(self, surface, transform=None):
        self.surface   = surface

        if transform is None:
            # no transform
            transform = Transform(surface[0].w, surface[0].h, 0,0, surface[0].w, surface[0].h)

        self.transform = transform

        self.font = None

        self.set_color(0xfffff08f)


    def set_color(self, color, mode="normal"):
        # get pointer to pixels as uint32[]
        u32_pixels = ctypes.cast(self.surface[0].pixels, ctypes.POINTER(ctypes.c_uint32))
        # get surface width
        width  = self.surface[0].w
        height = self.surface[0].h
        color  = 0xfffff08f

        self.put_pixel = lambda x,y: Canvas._draw_pixel(u32_pixels, width, height, x, y, color, mode)


    def clear(self):
        SDL_FillRect(self.surface, None, 0xFF000000) #black with 100% alpha (no transparency)

    def draw_pixel(self, x, y):
        sx,sy = self.transform.to_screen(x,y)
        self.put_pixel(sx,sy)


    def draw_line(self, x1,y1, x2,y2):

        sx1,sy1 = self.transform.to_screen(x1,y1)
        sx2,sy2 = self.transform.to_screen(x2,y2)

        Canvas._line(sx1,sy1,sx2,sy2, self.put_pixel)


    def draw_filled_circle(self,x,y,radius):
        sx,sy = self.transform.to_screen(x,y)
        radius = Transform.to_int(radius)
        Canvas._filled_circle(sx,sy,radius, self.put_pixel)

    def draw_circle(self, x, y, radius):
        sx,sy = self.transform.to_screen(x,y)
        radius = Transform.to_int(radius)
        Canvas._circle(sx,sy,radius, self.put_pixel)

    def draw_rectangle(self, x1, y1, x2, y2):
        self.draw_line(x1,y1,x1,y2)
        self.draw_line(x1,y1,x2,y1)
        self.draw_line(x2,y1,x2,y2)
        self.draw_line(x1,y2,x2,y2)

    def draw_text(self, x, y, text):

        if not self.font:
            self.font = TTF_OpenFont(b"fonts/ARCADE_R.TTF", 10)
            if not self.font:
                raise TTF_GetError()

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



    def draw_image(self, canvas, x=0, y=0):

        sx,sy = self.transform.to_screen(x,y)
        rcDest = SDL_Rect()
        rcDest.x = sx
        rcDest.y = sy
        rcDest.w = canvas.surface[0].w
        rcDest.h = canvas.surface[0].h

        SDL_BlitSurface(canvas.surface, None, self.surface, ctypes.byref(rcDest))


    def _draw_pixel(pixels,width,height,x,y,color,mode):
        if mode=="normal":
            Canvas._write_pixel(pixels,width,height,x,y,color)
        elif mode=="xor":
            prev_color = Canvas._read_pixel(pixels,width,height,x,y)
            new_color = (prev_color ^ color) | 0xFF000000
            Canvas._write_pixel(pixels,width,height,x,y, new_color)
        else:
            raise Exception(f"unknown draw pixel mode: {mode}")


    def _read_pixel(pixels,width,height, x,y):
        if x>=0 and y>=0 and x<width and y<height:
            return pixels[y*width + x]

    def _write_pixel(pixels,width,height, x,y, color32):
   #     print(f"width={width}, height={height}, x={x}, y={y}")
        if x>=0 and y>=0 and x<width and y<height:
            pixels[y*width + x] = color32


    # https://stackoverflow.com/questions/1201200/fast-algorithm-for-drawing-filled-circles
    def _filled_circle(x,y,r, putPixel):
        r2 = r * r
        area = r2 << 2
        rr = r << 1

        for i in range(area):
            tx = (i % rr) - r
            ty = (i / rr) - r
            if tx * tx + ty * ty <= r2:
                putPixel(int(x + tx), int(y + ty))


    def _circle(x0, y0, radius, putPixel):
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


    def _line(x0, y0, x1, y1, putPixel):

        # Bresenham's algorithm

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


class Image:
    def __init__(self, width, height, centerx=0, centery=0):
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
    def __init__(self, mode="VGA"):
        self.set_mode(mode)

        self.last_key = None
        self.last_mouse = None

        SDL_Init(SDL_INIT_EVERYTHING)
        TTF_Init()

        self.sprites = List(Sprite,20)
        self.images = {}

    def create_image(self, name, width, height, centerx, centery):
        image = Image(width,height,centerx,centery)
        self.images[name] = image
        return image



    def set_mode(self,mode):

        if mode == "SVGA":
            bkcolor = "#DFDFDF" #white
            width   = 800
            height  = 600
            scale_x = 1
            scale_y = 1
        elif mode == "VGA":
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


        self.window   = SDL_CreateWindow(b"SDL2 Window", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, width*scale_x, height*scale_y, SDL_WINDOW_SHOWN)
        self.renderer = SDL_CreateRenderer(self.window, -1, 0)


        surface = SDL_CreateRGBSurface(SDL_SWSURFACE, width, height, 32, 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000)
        surface_merged = SDL_CreateRGBSurface(SDL_SWSURFACE, width, height, 32, 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000)
        transform = Transform(width, height,  0, 200, 320, 0)
        self.canvas = Canvas(surface,transform)
        self.canvas_merged = Canvas(surface_merged,transform)

        self.texture  = None
        self.event    = SDL_Event()



    def start_draw(self):
        self.canvas.clear()
        self.sprites.clear()

    def draw_sprite(self, image_name, x, y):
        sprite = self.sprites.create()
        sprite.set(self.images[image_name], x, y)
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
                print(f"last mouse = {self.last_mouse}")

            elif self.event.type == SDL_KEYDOWN:
                self.last_key = self.event.key.keysym.sym
                print(f"last key = {self.last_key}")


    def check_key(self):
        ret_key = self.last_key
        self.last_key = None
        return ret_key

    def check_mouse(self):
        ret_mouse = self.last_mouse
        self.last_mouse = None
        return ret_mouse


