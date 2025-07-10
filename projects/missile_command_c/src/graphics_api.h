#ifndef GRAPHICS_API_H_
#define GRAPHICS_API_H_

#include "sdl/sdl_graphics_api.h"

#include "c6502.h"

struct tagCanvas;
typedef struct tagCanvas Canvas;

struct tagRect;
typedef struct tagRect Rect;


typedef struct tagMouseClick {
    U16 x;
    U16 y;
    U8 button;
} MouseClick;


#define MODE_NORMAL 1
#define MODE_XOR    2
#define MODE_ERASE  3


void Canvas_set_color(Canvas* pCanvas, U32 color, U8 mode, BOOLEAN erase_later);
void Canvas_write_pixel(Canvas* pCanvas, U16 x, U16 y, U32 color);
void Canvas_filled_rect(Canvas* pCanvas, Rect* pRect, U32 color);

#endif
