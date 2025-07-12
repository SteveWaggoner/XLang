#ifndef SDL_GRAPHICS_API_H_
#define SDL_GRAPHICS_API_H_

#include "../c6502.h"
#include "../list.h"
#include "../transform.h"


#include "SDL3/SDL.h"
#include "SDL3_ttf/SDL_ttf.h"

#define MODE_SVGA   1
#define MODE_VGA    2
#define MODE_C64_MC 3

typedef struct tagCanvas {
    SDL_Surface* surface;
    U32* pixels;
    U8 mode;
    U32 color;
} Canvas;

typedef struct tagImage {
    Canvas canvas;
    I16 centerx;
    I16 centery;
} Image;

typedef struct tagSprite {
    Item item;
    Image image;
    I16 x;
    I16 y;
} Sprite;

typedef struct {
    List list;
    Sprite alien[20];
} SpriteList;

typedef struct tagApp {
    U16 width;
    U16 height;
    U16 scale_x;
    U16 scale_y;

    Transform transform;

    TTF_Font* font;

    SDL_Window* window;
    SDL_Renderer* renderer;

    SpriteList sprites;
    Canvas canvas;
    Canvas canvas_merged;

} App;

#endif

