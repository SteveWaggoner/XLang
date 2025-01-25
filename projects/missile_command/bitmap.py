#!/usr/bin/python3.9


#
# purpose of this is to provide s simple graphic api that mimics
# the limitations of VERA in the X16 Commander
#
# The API isn't exactly the same as KERNAL but it close enough
# for design work
#


from graphics import GraphWin, Point, Image
import time, math, sys

from list import Item, List

import PIL.Image
import PIL.ImageTk

class Bitmap:

    def __init__(self, path=None, width=None, height=None, pil_img=None, color=None):

        if pil_img is not None:
            self.pil_img = pil_img
        else:
            if path is None:
                if type(color) == str:
                    color = hex2rgb(color)
                self.pil_img = PIL.Image.new(mode="RGB", size=(width, height), color=color)
            else:
                self.pil_img = PIL.Image.open(path)

    def resize(self, scale_x, scale_y):
        resized_image = self.pil_img.resize((self.width()*scale_x,self.height()*scale_y), 0)
        return Bitmap(pil_img=resized_image)


    def width(self):
        return self.pil_img.width

    def height(self):
        return self.pil_img.height


    def get_pixel(self, x, y):
        """Returns a list [r,g,b] with the RGB color values for pixel (x,y)
        r,g,b are in range(256)

        """
        color = self.pil_img.getpixel((x,y))
        return color


    def put_pixel(self, x, y, color, mode="copy"):
        """Sets pixel (x,y) to the given color

        """

        if x < 0 or y < 0 or x >= self.pil_img.width or y >= self.pil_img.height or color is None:
            return

        if type(color) == str:
            color = hex2rgb(color)

        if mode == "xor":
            prev_r, prev_g, prev_b, prev_a = self.get_pixel(x,y)
            r,g,b = color
            xor_color = (prev_r^r, prev_g^g, prev_b^b)
            color = xor_color

        self.pil_img.putpixel((x, y), color)


    def get_block(self, start_x, start_y, width, height):

        pixels = []
        for row in range(height):
            pixel_row = []
            for col in range(width):
                pixel_row.append(self.get_pixel(start_x+col, start_y+row))
            pixels.append(pixel_row)

        return pixels

    def put_block(self,x,y,pixels,mode="copy",flip_vert=False, flip_hort=False):
        for row in range(len(pixels)):
            for col in range(len(pixels[0])):
                if flip_vert:
                    i = len(pixels) - row - 1
                else:
                    i = row

                if flip_hort:
                    j = len(pixels[0]) - col - 1
                else:
                    j = col

                self.put_pixel(x+col,y+row, pixels[i][j], mode)

    def fill_rect(self, x,y,width,height,color):
        if type(color) == str:
            color = hex2rgb(color)

        for i in range(width):
            for j in range(height):
                self.put_pixel(x+i,y+j,color)




def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def hex2rgb(hexcode):
    if hexcode == "black":
        return (0,0,0)
    h = hexcode.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))



class TileMap:

    def __init__(self, path, cell_size_x, cell_size_y, offset_x=0, offset_y=0, trim_x=0, trim_y=0):

        self.img = Bitmap(path=path)
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.cells_per_row = self.img.width() // cell_size_x

        self.offset_x = offset_x
        self.offset_y = offset_y
        self.trim_x   = trim_x
        self.trim_y   = trim_y

        self.tile_cache = {}

    def get_tile(self, tile):

        if tile in self.tile_cache:
            return self.tile_cache[tile]

        start_x = (tile % self.cells_per_row) * self.cell_size_x
        start_y = (tile // self.cells_per_row) * self.cell_size_y
        tile_pixels = self.img.get_block(start_x + self.offset_x, start_y + self.offset_y,
                                  self.cell_size_x - self.trim_x, self.cell_size_y - self.trim_y)
        self.tile_cache[tile] = tile_pixels
        return tile_pixels



class WindowBitmap:

    def __init__(self, img = None, size_x=None, size_y=None, scale_x=None,scale_y=None, scale_to_win=None, color=None):

        if img is not None:
            self.img = img
        else:
            self.img = Bitmap(width=size_x, height=size_y, color=color)

        if scale_to_win is None:
            self.scale_x = scale_x
            self.scale_y = scale_y
        else:
            self.scale_x = scale_to_win.scale_x
            self.scale_y = scale_to_win.scale_y


    def get_image(self):
        resized_img = self.img.resize(self.scale_x, self.scale_y)

        #
        # this means anchor at (zero,zero) since point is relative to middle of photo
        #
        anchor_x = self.img.pil_img.width  // 2
        anchor_y = self.img.pil_img.height // 2


        image = Image(Point(anchor_x,anchor_y), resized_img.width(),resized_img.height())
        image.img = PIL.ImageTk.PhotoImage(resized_img.pil_img) # assign PhotoImage to PhotoImage
        return image

#
#
#
class Sprite(Item):
    def __init__(self):
        super().__init__()
        self.tilemap = None
        self.tile_start = None
        self.tile_end = None

    def get_tile(self, n):
        tile = (n + self.tile_start) % (self.tile_end - self.tile_start)
        return self.tilemap.get_tile(tile)

class Window:
    def __init__(self, mode="VGA"):
        self.set_mode(mode)
        self.sprites = List(Sprite,15)

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

        self.scale_x = scale_x
        self.scale_y = scale_y

        self.win = GraphWin(width = width*scale_x, height = height*scale_y, autoflush = False) # scaled-up a window
        self.win.setCoords(0, height, width, 0)  #invert the y coordinate
        self.background = WindowBitmap(size_x=width, size_y=height, scale_x=scale_x, scale_y=scale_y, color=bkcolor)
        self.last_bkgnd = None

    def draw_background(self):

        if not self.last_bkgnd is None:
            self.last_bkgnd.undraw()
        self.last_bkgnd = self.background.get_image()
        self.last_bkgnd.draw(self.win)


    def checkMouse(self):
        return self.win.checkMouse()

    def checkKey(self):
        return self.win.checkKey()

    def redraw(self):
        self.win.redraw()

    def flush(self):
        self.win.flush()

    def wait_for_key(self):
        self.win.getKey()




def main():

    window = Window("VGA")

    black  = "#000000"
    yellow = "#FFFFE0"
    pink   = "#FFC0CB"

    tilemap = TileMap(path="./images/mario.png",cell_size_x=50,cell_size_y=50, offset_x=1, offset_y=1)
    mario = Sprite(tilemap, 0, 8)

    bkgnd = window.background
    for n in range(10):
        frame = mario.get_tile(n)
        bkgnd.img.put_block(5+n,5+n, frame)
        bkgnd.img.put_pixel(5+n,5+n, black)
        window.draw_background()
        window.flush()
        window.wait_for_key()

    for x in range(10):
        frame = mario.get_tile(x)
        bkgnd.img.put_block(5+n-x,5+n+x, frame, flip_hort=True)
        bkgnd.img.put_pixel(5+n-x,5+n+x, black)
        window.update()
        window.flush()
        window.wait_for_key()

if __name__=="__main__":
    main()
