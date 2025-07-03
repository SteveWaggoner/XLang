class Image:

    global_palette = []


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

        self.width  = width
        self.height = height
        self.centerx = centerx
        self.centery = centery
        self.pixels_len = len(pixels)
        #palette-ize
        self.palette = []
        self.pixels = []
        for i, c in enumerate(pixels):

            try:
                global_pal_index = Image.global_palette.index(c)
            except ValueError:
                global_pal_index = len(Image.global_palette)
                Image.global_palette.append(c)

            try:
                pal_index = self.palette.index(global_pal_index)
            except ValueError:
                pal_index = len(self.palette)
                self.palette.append(global_pal_index)

            self.pixels.append(pal_index)

        self.palette_len = len(self.palette)


        print(f"found {len(self.palette)} unique colors")








#        self.image = Image(width,height,centerx,centery)
#        for i, c in enumerate(pixels):
#            self.image.canvas.pixels[i] = c

def get_c_type(val, name):
    if isinstance(val, int):
        if val >= 0 and val < 256: return f"const unsigned char {name}"
        if val >= 0 and val < 256*256: return f"const unsigned short {name}"
        if val >= 0 and val < 256*256*256*256: return f"const unsigned long {name}"

    if isinstance(val, list):
        return f"{get_c_type(max(val),name)}[{len(val)}]"

def get_c_val(val):
    if isinstance(val, int):
        if val >= 0 and val < 256: return val
        if val >= 0 and val < 256*256: return val
        if val >= 0 and val < 256*256*256*256: return hex(val)

    return val



def main():

    # https://stackoverflow.com/questions/2601047/import-a-python-module-without-the-py-extension/43602645#43602645
    from importlib.util import spec_from_loader, module_from_spec
    from importlib.machinery import SourceFileLoader

    spec = spec_from_loader("game_sprites", SourceFileLoader("game_sprites", "./game_sprites.assets"))
    assets = module_from_spec(spec)
    spec.loader.exec_module(assets)

    for attr_name in vars(assets):
        attr_type = type(getattr(assets,attr_name)).__name__

        if attr_type == "Image":
            img = getattr(assets, attr_name)
            for img_attr in vars(img):
                img_varname = f"{assets.__name__}__{attr_name}_{img_attr}"
                img_val = getattr(img,img_attr)
                print(f"{get_c_type(img_val,img_varname)} = {get_c_val(img_val)};")

if __name__=="__main__":
    main()

