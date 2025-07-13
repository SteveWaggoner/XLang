#ifndef GRAPHICS_API_H_
#define GRAPHICS_API_H_


#include "c6502.h"

struct tagCanvas;
typedef struct tagCanvas Canvas;

typedef struct tagRect {
        I16 x, y;
        I16 w, h;
} Rect;

typedef struct tagMouseClick {
    I16 x;
    I16 y;
    U8 button;
} MouseClick;


#define CANVAS_MODE_NORMAL 1
#define CANVAS_MODE_XOR    2


void App_init(U8* title, U8 mode);
void App_poll_events();
I16 App_check_key();
MouseClick* App_check_mouse();
Canvas* App_canvas();

void Canvas_set_color(Canvas* pCanvas, U32 color, U8 mode);
void Canvas_write_pixel(Canvas* pCanvas, U16 x, U16 y, U32 color);
void Canvas_filled_rect(Canvas* pCanvas, Rect* pRect, U32 color);
void Canvas_draw_pixel(Canvas* pCanvas, U16 x, U16 y);

#include "sdl/sdl_graphics_api.h"


#endif
