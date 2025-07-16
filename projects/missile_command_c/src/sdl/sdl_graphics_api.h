#ifndef SDL_GRAPHICS_API_H_
#define SDL_GRAPHICS_API_H_

#include "../c6502.h"
#include "../list.h"
#include "../transform.h"


#include "SDL3/SDL.h"
#include "SDL3_ttf/SDL_ttf.h"

#define APP_MODE_SVGA   1
#define APP_MODE_VGA    2
#define APP_MODE_C64_MC 3

typedef struct tagCanvas {
    SDL_Surface* surface;
    U32* pixels;
    U8 mode;
    U32 color;
} Canvas;


typedef struct tagApp {
    U16 width;
    U16 height;
    U16 scale_x;
    U16 scale_y;

    Transform transform;

    TTF_Font* font;

    SDL_Window* window;
    SDL_Renderer* renderer;
    SDL_Event event;
    SDL_Texture* texture;

    U8 has_mouse_click;
    U8 has_key;
    MouseClick last_mouse_click;
    I16 last_key;

    Sprite sprites[4];
    Canvas canvas;
    Canvas canvas_merged;

} App;


#endif

