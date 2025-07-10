#ifndef SDL_GRAPHICS_API_H_
#define SDL_GRAPHICS_API_H_

#include "../c6502.h"

#include "SDL3/SDL.h"
#include "SDL3_ttf/SDL_ttf.h"

// Internal class for 2-D coordinate transformations
typedef struct tagWindow {
    U16 xbase;
    U16 ybase;
    U16 xscale;
    U16 yscale;
} Window;

typedef struct tagImage {
    U16 xbase;
    U16 ybase;
    U16 xscale;
    U16 yscale;
} Image;


#endif

