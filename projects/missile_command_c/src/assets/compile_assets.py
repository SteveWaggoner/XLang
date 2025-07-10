#!/usr/bin/env python3.8

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

        print(Image.global_palette)
        print(f"found {len(self.palette)} unique colors")


def get_c_type(val, name):
    if isinstance(val, int):
        if val >= 0 and val < 256: return f"const unsigned char {name}"
        if val >= 0 and val < 256*256: return f"const unsigned short {name}"
        if val >= 0 and val < 256*256*256*256: return f"const unsigned long {name}"

    if isinstance(val, list):
        return f"{get_c_type(max(val),name)}[{len(val)}]"

def get_c_val(val):
    if isinstance(val, int):
        if val >= 0 and val < 256: return str(val)
        if val >= 0 and val < 256*256: return str(val)
        if val >= 0 and val < 256*256*256*256: return hex(val)

    if isinstance(val, list):
        arr = []
        for x in val:
            arr.append(get_c_val(x))
        return "{" + (", ".join(arr)) + "}"

    return f"<{val}>"



def write_asset_value(varname, val, output_h, output_c):
    print(f"{get_c_type(val,varname)} = {get_c_val(val)};", file=output_c)
    print(f"extern {get_c_type(val,varname)};", file=output_h)

import os, glob
def compile_asset_file(path, output_h, output_c):

    print("compiling "+path)

    # https://stackoverflow.com/questions/678236/how-do-i-get-the-filename-without-the-extension-from-a-path-in-python
    filename = os.path.splitext(os.path.basename(path))[0]

    # https://stackoverflow.com/questions/2601047/import-a-python-module-without-the-py-extension/43602645#43602645
    from importlib.util import spec_from_loader, module_from_spec
    from importlib.machinery import SourceFileLoader

    spec = spec_from_loader(filename, SourceFileLoader(filename, path))
    assets = module_from_spec(spec)
    spec.loader.exec_module(assets)

    asset_name = assets.__name__

    for attr_name in vars(assets):
        attr_type = type(getattr(assets,attr_name)).__name__
        if attr_type == "Image":

            class_name = attr_name

            print("", file=output_c)
            print("", file=output_h)

            img = getattr(assets, attr_name)
            for img_attr in vars(img):
                img_varname = f"{asset_name}__{class_name}_{img_attr}"
                img_val = getattr(img,img_attr)
                write_asset_value(img_varname, img_val, output_h, output_c)

    print("", file=output_c)
    print("", file=output_h)
    write_asset_value(f"{asset_name}__global_palette", assets.Image.global_palette, output_h, output_c)
    write_asset_value(f"{asset_name}__global_palette_len", len(assets.Image.global_palette), output_h, output_c)




def main():
    output_h_path = "assets.h"
    output_c_path = "assets.c"

    with open(output_c_path, "w") as output_c, open(output_h_path,"w") as output_h:

        print(f"#include \"{output_h_path}\"", file=output_c)

        for asset_path in glob.glob("./*.assets"):
            compile_asset_file(asset_path, output_h, output_c)


if __name__=="__main__":
    main()

