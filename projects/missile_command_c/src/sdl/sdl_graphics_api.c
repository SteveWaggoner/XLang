
#include "../graphics_api.h"

#include "../transform.h"

#include <assert.h>

#define MAX_ERASE_LEN 5000

typedef struct tagCanvas {
    Transform transform;
    TTF_Font* font;

    SDL_Surface* surface;
    U32* pixels;
    U16 width;
    U16 height;

    SDL_Surface* bkgnd_surface;
    U32* bkgnd_pixels;
    U16 bkgnd_width;
    U16 bkgnd_height;

    U8 mode;
    U32 color;
    BOOLEAN erase_later;

    U32 erase_list_cnt;
    U16 erase_list_x[MAX_ERASE_LEN];
    U16 erase_list_y[MAX_ERASE_LEN];

} Canvas;

Transform g_no_transform;
void Canvas_init(Canvas* pCanvas, SDL_Surface* surface, SDL_Surface* bkgnd_surface) {

    // no transform
    Transform_init(&pCanvas->transform, surface[0].w, surface[0].h, 0, 0, surface[0].w, surface[0].h);

    pCanvas->surface = surface;
    pCanvas->bkgnd_surface = bkgnd_surface;
    pCanvas->font = 0;

    Canvas_set_color(pCanvas, 0xfffff08f, pCanvas->mode, pCanvas->erase_later);

    // get pointer to pixels as uint32[]
    pCanvas->pixels = surface[0].pixels;
    // get surface width
    pCanvas->width = surface[0].w;
    pCanvas->height = surface[0].h;

    if (bkgnd_surface) {
        pCanvas->bkgnd_pixels = bkgnd_surface[0].pixels;
        pCanvas->bkgnd_width = bkgnd_surface[0].w;
        pCanvas->bkgnd_height = bkgnd_surface[0].h;
    }
    else {
        pCanvas->bkgnd_width = 0;
        pCanvas->bkgnd_height = 0;
    }
    pCanvas->erase_list_cnt = 0;
}


void Canvas_set_color(Canvas* pCanvas, U32 color, U8 mode, BOOLEAN erase_later) {
    pCanvas->color = color;
    pCanvas->mode = mode;
    pCanvas->erase_later = erase_later;
}

void Canvas_put_pixel(Canvas* pCanvas, U16 x, U16 y) {

    switch (pCanvas->mode) {

    case MODE_NORMAL:
    {
        Canvas_write_pixel(pCanvas, x, y, pCanvas->color);
        break;
    }

    case MODE_XOR:
    {
        U32 old_color = Canvas_read_pixel(pCanvas, x, y);
        U32 new_color = (old_color ^ pCanvas->color) | 0xFF000000;
        Canvas_write_pixel(pCanvas, x, y, new_color);
        break;
    }

    case MODE_ERASE:
    {
        U32 bkgnd_color = Canvas_read_bkgnd_pixel(pCanvas, x, y);
        Canvas_write_pixel(pCanvas, x, y, bkgnd_color);
        break;
    }
    default:
        printf("Unknown put_pixel mode %d\n", pCanvas->mode);
    }
}

U32 Canvas_read_pixel(Canvas* pCanvas, U16 x, U16 y) {
    if (x < pCanvas->width && y < pCanvas->height) {
        return pCanvas->pixels[y * pCanvas->width + x];
    }
    else {
        return 0;
    }
}

U32 Canvas_read_bkgnd_pixel(Canvas* pCanvas, U16 x, U16 y) {
    if (x < pCanvas->width && y < pCanvas->height) {
        return pCanvas->bkgnd_pixels[y * pCanvas->width + x];
    }
    else {
        return 0;
    }
}

void Canvas_write_pixel(Canvas* pCanvas, U16 x, U16 y, U32 color) {
    if (x < pCanvas->width && y < pCanvas->height) {
        pCanvas->pixels[y * pCanvas->width + x] = color;
    }
}

void Canvas_write_bkgnd_pixel(Canvas* pCanvas, U16 x, U16 y, U32 color) {
    if (x < pCanvas->width && y < pCanvas->height) {
        pCanvas->bkgnd_pixels[y * pCanvas->width + x] = color;
    }
}


void Canvas_clear(Canvas* pCanvas) {
    Canvas_filled_rect(pCanvas, NULL, 0xFF000000); //black with 100 % alpha(no transparency)
}

void Canvas_clear_bkgnd(Canvas* pCanvas, void* rect, U32 color32) {
    SDL_FillSurfaceRect(pCanvas->bkgnd_surface, rect, color32);
}


void Canvas_filled_rect(Canvas* pCanvas, Rect* pRect, U32 color) {
    SDL_FillSurfaceRect(pCanvas->surface, pRect, color);
}


void Canvas_draw_pixel(Canvas* pCanvas, U16 x, U16 y) {
    U16 sx, sy;
    Transform_to_screen(&pCanvas->transform, x, y, &sx, &sy);

    Canvas_put_pixel(pCanvas, sx, sy);
    if (pCanvas->erase_later) {

        assert(pCanvas->erase_list_cnt < MAX_ERASE_LEN);

        pCanvas->erase_list_x[pCanvas->erase_list_cnt] = sx;
        pCanvas->erase_list_y[pCanvas->erase_list_cnt] = sy;
        pCanvas->erase_list_cnt++;
    }

}

void Canvas_draw_line(Canvas* pCanvas, U16 x1, U16 y1, U16 x2, U16 y2) {
    U16 sx1, sy1, sx2, sy2;
    Transform_to_screen(&pCanvas->transform, x1, y1, &sx1, &sy1);
    Transform_to_screen(&pCanvas->transform, x2, y2, &sx2, &sy2);
    Shape_line(sx1, sy1, sx2, sy2, Canvas_put_pixel, pCanvas);
}

void Canvas_draw_filled_circle(Canvas* pCanvas, U16 x, U16 y, U16 radius) {
    U16 sx, sy;
    Transform_to_screen(&pCanvas->transform, x, y, &sx, &sy);
    Shade_filled_circle(sx, sy, radius, Canvas_put_pixel, pCanvas);
}

void Canvas_draw_filled_octogon(Canvas* pCanvas, U16 x, U16 y, U16 radius, U8 slope_dx, U8 slope_dy) {
    U16 sx, sy;
    Transform_to_screen(&pCanvas->transform, x, y, &sx, &sy);
    Shape_filled_octogon(sx, sy, radius, slope_dx, slope_dy, Canvas_put_pixel, pCanvas);
}

void Canvas_draw_circle(Canvas* pCanvas, U16 x, U16 y, U16  radius) {
    U16 sx, sy;
    Transform_to_screen(&pCanvas->transform, x, y, &sx, &sy);
    Shape_circle(sx, sy, radius, Canvas_put_pixel, pCanvas);
}

void Canvas_draw_rectangle(Canvas* pCanvas, U16 x1, U16 y1, U16 x2, U16 y2) {
    U16 sx1, sy1, sx2, sy2;
    Transform_to_screen(&pCanvas->transform, x1, y1, &sx1, &sy1);
    Transform_to_screen(&pCanvas->transform, x2, y2, &sx2, &sy2);

    Shape_line(sx1, sy1, sx1, sy2, Canvas_put_pixel, pCanvas);
    Shape_line(sx1, sy1, sx2, sy1, Canvas_put_pixel, pCanvas);
    Shape_line(sx2, sy1, sx2, sy2, Canvas_put_pixel, pCanvas);
    Shape_line(sx1, sy2, sx2, sy2, Canvas_put_pixel, pCanvas);
}

void Canvas_draw_text(Canvas* pCanvas, U16 x, U16 y, U8* text) {

    if (!pCanvas->font) {
        pCanvas->font = TTF_OpenFont("fonts/ARCADE_R.TTF", 8);
        if (!pCanvas->font) {
            printf("TTF_OpenFont() error = %s\n", SDL_GetError());
        }
    }

    // Create surface with rendered text
    SDL_Color textColor = { 0,0,0,0 };
    textColor.r = 100;
    textColor.g = 110;
    textColor.b = 160;

    SDL_Surface* textSurface = TTF_RenderText_Solid(pCanvas->font, text, strlen(text), textColor);
    if (!textSurface) {
        printf("Failed to create text surface: %s\n", SDL_GetError());
    }

    U16 sx, sy;
    Transform_to_screen(&pCanvas->transform, x, y, &sx, &sy);

    SDL_Rect rcDest = { 0,0,0,0 };
    rcDest.x = sx;
    rcDest.y = sy;
    rcDest.w = textSurface[0].w;
    rcDest.h = textSurface[0].h;

    SDL_BlitSurface(textSurface, NULL, pCanvas->surface, &rcDest);
    SDL_DestroySurface(textSurface);

    if (pCanvas->erase_later) {
        U32 bkgnd_color = Canvas_read_bkgnd_pixel(pCanvas, sx, sy);
    //    self.erase_list.append(lambda : self._filled_rect(rcDest, bkgnd_color));
    }
}

void Canvas_draw_image(Canvas* pCanvas, Canvas* pImage, U16 x, U16 y) {

    U16 sx, sy;
    Transform_to_screen(&pCanvas->transform, x, y, &sx, &sy);
    SDL_Rect rcDest = { 0,0,0,0 };
    rcDest.x = sx;
    rcDest.y = sy;
    rcDest.w = pCanvas->surface[0].w;
    rcDest.h = pCanvas->surface[0].h;

    SDL_BlitSurface(pImage->surface, NULL, pCanvas->surface, &rcDest);

    if (pCanvas->erase_later) {
        U32 bkgnd_color = Canvas_read_bkgnd_pixel(pCanvas, sx, sy);
        //self.erase_list.append(lambda : self._filled_rect(rcDest, bkgnd_color))
    }
}

