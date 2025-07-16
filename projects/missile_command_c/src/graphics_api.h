#ifndef GRAPHICS_API_H_
#define GRAPHICS_API_H_


#include "c6502.h"
#include "list.h"

struct tagCanvas;
typedef struct tagCanvas Canvas;

typedef struct tagSprite {
    BOOLEAN active;
    Canvas* canvas;
    I16 x;
    I16 y;
    I16 centerx;
    I16 centery;
} Sprite;

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


void        App_init(U8* title, U8 mode);
void        App_finish_draw();
void        App_poll_events();
I16         App_check_key();
MouseClick* App_check_mouse();
Canvas*     App_canvas();
Sprite*     App_sprite(U16 width, U16 height);

U32  Canvas_read_pixel    (Canvas* canvas, U16 x, U16 y);
void Canvas_write_pixel   (Canvas* canvas, U16 x, U16 y, U32 color);
void Canvas_filled_rect   (Canvas* canvas, Rect* pRect,  U32 color);

void Canvas_set_color     (Canvas* canvas, U32 color, U8 mode);
void Canvas_clear         (Canvas* canvas);
void Canvas_draw_pixel    (Canvas* canvas, I16 x,  I16 y);
void Canvas_draw_line     (Canvas* canvas, I16 x1, I16 y1, I16 x2, I16 y2);
void Canvas_draw_circle   (Canvas* canvas, I16 x,  I16 y,  I16  radius);
void Canvas_draw_rectangle(Canvas* canvas, I16 x1, I16 y1, I16 x2, I16 y2);

void Canvas_draw_filled_circle (Canvas* canvas, I16 x, I16 y, I16 radius);
void Canvas_draw_filled_octogon(Canvas* canvas, I16 x, I16 y, I16 radius, float slope_dx, float slope_dy);

void Canvas_draw_text     (Canvas* canvas, I16 x, I16 y, U8* text);
void Canvas_draw_image    (Canvas* canvas, Canvas* image, I16 x, I16 y);

#include "sdl/sdl_graphics_api.h"


#endif
