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


def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def hex2rgb(hexcode):
    print(hexcode)
    h = hexcode.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


class SimpleImage:

    def __init__(self, path=None, width=None, height=None, photo_img=None):

        if photo_img is not None:
            self.photo_img = photo_img
        else:

            from graphics import _root
            try:  # import as appropriate for 2.x vs. 3.x
                import tkinter as tk
            except:
                import Tkinter as tk

            if path is None:
                self.photo_img = tk.PhotoImage(master=_root, width=width, height=height)
            else:
                self.photo_img = tk.PhotoImage(master=_root, file=path)


    def resized_image(self, scale_x, scale_y):

        resized_image = self.photo_img.copy()
        return SimpleImage(photo_img=resized_image.zoom(scale_x, scale_y))


    def width(self):
        return self.photo_img.width()

    def height(self):
        return self.photo_img.height()



    def get_pixel(self, x, y):
        """Returns a list [r,g,b] with the RGB color values for pixel (x,y)
        r,g,b are in range(256)

        """

        color = self.photo_img.get(x,y)
        red, green, blue = color
        color = rgb2hex(red,blue,green)

        return color



    def put_pixel(self, x, y, color, mode="copy"):
        """Sets pixel (x,y) to the given color

        """

        if x < 0 or y < 0 or color is None:
            return

        if mode == "xor":
            prev_color = self.get_pixel(x,y)
            prev_r,prev_g,prev_b = hex2rgb(prev_color)
            r,g,b = hex2rgb(color)
            xor_color = rgb2hex(prev_r^r, prev_g^g, prev_b^b)

            print(prev_color+" --> "+xor_color)
            color  = xor_color

        self.photo_img.put(color, (x, y))



class TileMap:

    def __init__(self, path, cell_size_x, cell_size_y):

        self.img = SimpleImage(path=path)
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.cells_per_row = self.img.width() // cell_size_x

    def get_pixels(self, tile):

        start_x = (tile % self.cells_per_row) * self.cell_size_x
        start_y = (tile // self.cells_per_row) * self.cell_size_y

        pixels = []
        for row in range(self.cell_size_y):
            pixel_row = []
            for col in range(self.cell_size_x):
                pixel_row.append(self.img.get_pixel(start_x+col, start_y+row))
            pixels.append(pixel_row)

        return pixels


class Bitmap:

    def __init__(self,
                 size_x,size_y,
                 anchor_x=None,anchor_y=None,
                 scale_x=None,scale_y=None,
                 pos_x=None,pos_y=None,
                 colors=None,
                 pixels=None):


        self.img = SimpleImage(width=size_x, height=size_y)

        self.scale_x = scale_x
        self.scale_y = scale_y

    def get_image(self):
        resized_img = self.img.resized_image(self.scale_x, self.scale_y)

        #
        # this means anchor at (zero,zero) since point is relative to middle of photo
        #
        anchor_x = self.img.photo_img.width()  // 2
        anchor_y = self.img.photo_img.height() // 2


        image = Image(Point(anchor_x,anchor_y), resized_img.width(),resized_img.height())
        image.img = resized_img.photo_img # assign PhotoImage to PhotoImage
        return image


    #bitmap api
    def fill_rect(self, x,y,width,height,color):
        for i in range(width):
            for j in range(height):
                self.img.put_pixel(x+i,y+j,color)

    def bit_blt(self,x,y,pixels,mode):

        print(pixels[0])

        for row in range(len(pixels)):
            for col in range(len(pixels[0])):
                self.img.put_pixel(x+col,y+row, pixels[row][col], mode)


    def fill_pixels(self, x,y,numPixels,color):
        pass


    def get_pixels(self, x,y,numPixels):
        pass

    def put_pixels(self, x,y,numPixels,pixelBuffer,maskBuffer,transparentColor,rasterOperation):
        pass

    def get_block(self, x,y,width,height):
        pass

    def put_block(self, x,y,width,height,pixelBuffer,maskBuffer,transparentColor,rasterOperation):
        pass

    def draw_text(self, x,y, text):
        pass


class Sprite:
    def __init__(self, bitmap, x,y):
        pass

class Window:
    def __init__(self, mode="VGA"):
        self.set_mode(mode)

    def set_mode(self,mode):

        if mode == "VGA":
            width   = 320
            height  = 200
            scale_x = 4
            scale_y = 4
        elif mode == "C64_MC":
            width   = 160
            height  = 200
            scale_x = 8
            scale_y = 4

        self.win = GraphWin(width = width*scale_x, height = height*scale_y, autoflush = False) # scaled-up a window
        self.win.setCoords(0, height, width, 0)  #invert the y coordinate
        self.background = Bitmap(size_x=width, size_y=height, scale_x=scale_x, scale_y=scale_y)
        self.last_bkgnd = None

    def set_background_color(self, color):
        self.background_color = color


    def update(self):

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

    window.set_background_color(black)

    tilemap = TileMap(path="./images/cards.gif",cell_size_x=40,cell_size_y=57)
    alien   = Bitmap(size_x=16,size_y=16, anchor_x=0, anchor_y=0, pixels=tilemap.get_pixels(0))
    sprite1 = Sprite(bitmap=alien, x=45, y=56)
    sprite2 = Sprite(bitmap=alien, x=67, y=78)

    bkgnd = window.background

    bkgnd.img.put_pixel(0,0,yellow)
    bkgnd.img.put_pixel(0,1,yellow)
    bkgnd.img.put_pixel(1,0,yellow)
    bkgnd.img.put_pixel(1,1,yellow)
    bkgnd.img.put_pixel(2,0,yellow)
    bkgnd.img.put_pixel(2,1,yellow)

    bkgnd.fill_rect(60,60, 81,117,pink)
#    bkgnd.fill_rect(290,190, 5,5,"yellow")
#    bkgnd.fill_rect(290,190, 2,2,"#2a2e00")
    bkgnd.fill_rect(250,190, 2,2,"blue")
    bkgnd.fill_rect(200,190, 2,2,"#2a2e00")
    bkgnd.fill_rect(319,199, 2,2,"blue")
#    bkgnd.fill_rect(0,0, 2,2,  "#2adee0")

    bkgnd.bit_blt(80,80, tilemap.get_pixels(0), "copy")
    bkgnd.bit_blt(90,90, tilemap.get_pixels(1), "copy")
    bkgnd.bit_blt(100,100, tilemap.get_pixels(2),"copy")


    bkgnd.bit_blt(85,85, tilemap.get_pixels(0), mode="xor")
    window.update()
    window.wait_for_key()

    bkgnd.bit_blt(85,85, tilemap.get_pixels(0), mode="xor")
    window.update()
    window.wait_for_key()

    bkgnd.bit_blt(85,85, tilemap.get_pixels(0), mode="xor")
    window.update()
    window.wait_for_key()

    bkgnd.bit_blt(85,85, tilemap.get_pixels(0), mode="xor")
    window.update()
    window.wait_for_key()

    bkgnd.bit_blt(85,85, tilemap.get_pixels(0), mode="xor")
    window.update()
    window.wait_for_key()

    bkgnd.bit_blt(85,85, tilemap.get_pixels(0), mode="xor")
    window.update()
    window.wait_for_key()

if __name__=="__main__":
    main()
