
#include "../graphics_api.h"

#include "../shape.h"


#include <assert.h>

void Canvas_init(Canvas* pCanvas, SDL_Surface* surface) {
    assert(pCanvas);
    assert(surface);
    pCanvas->surface = surface;
    pCanvas->pixels = surface->pixels;
    pCanvas->mode = 0;
    pCanvas->color = 0xfffff08f;
}

void Image_init(Image* pImage, I16 width, U16 height, U16 centerx, U16 centery) {

    SDL_Surface* surface = SDL_CreateSurface(width, height, SDL_PIXELFORMAT_ARGB8888);
    Canvas_init(&pImage->canvas, surface);
        
    pImage->centerx = centerx;
    pImage->centery = centery;
}


void Sprite_init(Sprite* pSprite, U16 width, U16 height) {
    Item_init(&pSprite->item);
    Image_init(&pSprite->image, width, height, 0, 0);
    pSprite->x = 0;
    pSprite->y = 0;
}


App g_app = { 0,0,0,0 };
void App_init(U8* title, U8 mode) {

    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO | SDL_INIT_JOYSTICK | SDL_INIT_EVENTS | SDL_INIT_SENSOR | SDL_INIT_GAMEPAD);
    TTF_Init();

    switch (mode)
    {
    case MODE_SVGA:
    {
        g_app.width = 800;
        g_app.height = 600;
        g_app.scale_x = 1;
        g_app.scale_y = 1;
        break;
    }
    case MODE_VGA:
    {
        g_app.width = 320;
        g_app.height = 200;
        g_app.scale_x = 4;
        g_app.scale_y = 4;
        break;
    }
    case MODE_C64_MC:
    {
        g_app.width = 160;
        g_app.height = 200;
        g_app.scale_x = 8;
        g_app.scale_y = 4;
        break;
    }
    default:
    {
        printf("Unknown mode: %d\n", mode);
    }
    }

    g_app.window = SDL_CreateWindow(title, SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, g_app.width * g_app.scale_x, g_app.height * g_app.scale_y, 0);
    g_app.renderer = SDL_CreateRenderer(g_app.window, -1, 0);

    Transform_init(&g_app.transform, g_app.width, g_app.height, 0, 200, 320, 0);

    INIT_LIST(Sprite, g_app.sprites, FALSE);


    SDL_Surface* surface = SDL_CreateSurface(g_app.width, g_app.height, SDL_PIXELFORMAT_ARGB8888);
    Canvas_init(&g_app.canvas, surface);

    SDL_Surface* surface_merged = SDL_CreateSurface(g_app.width, g_app.height, SDL_PIXELFORMAT_ARGB8888);
    Canvas_init(&g_app.canvas_merged, surface_merged);
}


void Canvas_set_color(Canvas* pCanvas, U32 color, U8 mode) {
    pCanvas->color = color;
    pCanvas->mode = mode;
}

void Canvas_put_pixel(Canvas* pCanvas, U16 x, U16 y) {

    switch (pCanvas->mode) {

    case CANVAS_MODE_NORMAL:
    {
        Canvas_write_pixel(pCanvas, x, y, pCanvas->color);
        break;
    }

    case CANVAS_MODE_XOR:
    {
        U32 old_color = Canvas_read_pixel(pCanvas, x, y);
        U32 new_color = (old_color ^ pCanvas->color) | 0xFF000000;
        Canvas_write_pixel(pCanvas, x, y, new_color);
        break;
    }

    default:
        printf("Unknown put_pixel mode %d\n", pCanvas->mode);
    }
}

U32 Canvas_read_pixel(Canvas* pCanvas, U16 x, U16 y) {
    I16 width = pCanvas->surface->w;
    if (x < width && y < pCanvas->surface->h) {
        return pCanvas->pixels[y * width + x];
    }
    else {
        return 0;
    }
}

void Canvas_write_pixel(Canvas* pCanvas, U16 x, U16 y, U32 color) {
    I16 width = pCanvas->surface->w;
    if (x < width && y < pCanvas->surface->h) {
        pCanvas->pixels[y * width + x] = color;
    }
}


void Canvas_clear(Canvas* pCanvas) {
    Canvas_filled_rect(pCanvas, NULL, 0xFF000000); //black with 100 % alpha(no transparency)
}

void Canvas_filled_rect(Canvas* pCanvas, Rect* pRect, U32 color) {
    SDL_FillSurfaceRect(pCanvas->surface, pRect, color);
}

void Canvas_draw_pixel(Canvas* pCanvas, U16 x, U16 y) {
    U16 sx, sy;
    Transform_to_screen(&g_app.transform, x, y, &sx, &sy);

    Canvas_put_pixel(pCanvas, sx, sy);
}

void Canvas_draw_line(Canvas* pCanvas, U16 x1, U16 y1, U16 x2, U16 y2) {
    U16 sx1, sy1, sx2, sy2;
    Transform_to_screen(&g_app.transform, x1, y1, &sx1, &sy1);
    Transform_to_screen(&g_app.transform, x2, y2, &sx2, &sy2);
    Shape_line(sx1, sy1, sx2, sy2, Canvas_put_pixel, pCanvas);
}

void Canvas_draw_filled_circle(Canvas* pCanvas, U16 x, U16 y, U16 radius) {
    U16 sx, sy;
    Transform_to_screen(&g_app.transform, x, y, &sx, &sy);
    Shape_filled_circle(sx, sy, radius, Canvas_put_pixel, pCanvas);
}

void Canvas_draw_filled_octogon(Canvas* pCanvas, U16 x, U16 y, U16 radius, U8 slope_dx, U8 slope_dy) {
    U16 sx, sy;
    Transform_to_screen(&g_app.transform, x, y, &sx, &sy);
    Shape_filled_octogon(sx, sy, radius, slope_dx, slope_dy, Canvas_put_pixel, pCanvas);
}

void Canvas_draw_circle(Canvas* pCanvas, U16 x, U16 y, U16  radius) {
    U16 sx, sy;
    Transform_to_screen(&g_app.transform, x, y, &sx, &sy);
    Shape_circle(sx, sy, radius, Canvas_put_pixel, pCanvas);
}

void Canvas_draw_rectangle(Canvas* pCanvas, U16 x1, U16 y1, U16 x2, U16 y2) {
    U16 sx1, sy1, sx2, sy2;
    Transform_to_screen(&g_app.transform, x1, y1, &sx1, &sy1);
    Transform_to_screen(&g_app.transform, x2, y2, &sx2, &sy2);

    Shape_line(sx1, sy1, sx1, sy2, Canvas_put_pixel, pCanvas);
    Shape_line(sx1, sy1, sx2, sy1, Canvas_put_pixel, pCanvas);
    Shape_line(sx2, sy1, sx2, sy2, Canvas_put_pixel, pCanvas);
    Shape_line(sx1, sy2, sx2, sy2, Canvas_put_pixel, pCanvas);
}

void Canvas_draw_text(Canvas* pCanvas, U16 x, U16 y, U8* text) {

    if (!g_app.font) {
        g_app.font = TTF_OpenFont("fonts/ARCADE_R.TTF", 8);
        if (!g_app.font) {
            printf("TTF_OpenFont() error = %s\n", SDL_GetError());
        }
    }

    // Create surface with rendered text
    SDL_Color textColor = { 0,0,0,0 };
    textColor.r = 100;
    textColor.g = 110;
    textColor.b = 160;

    SDL_Surface* textSurface = TTF_RenderText_Solid(g_app.font, text, strlen(text), textColor);
    if (!textSurface) {
        printf("Failed to create text surface: %s\n", SDL_GetError());
    }

    U16 sx, sy;
    Transform_to_screen(&g_app.transform, x, y, &sx, &sy);

    SDL_Rect rcDest = { 0,0,0,0 };
    rcDest.x = sx;
    rcDest.y = sy;
    rcDest.w = textSurface[0].w;
    rcDest.h = textSurface[0].h;

    SDL_BlitSurface(textSurface, NULL, pCanvas->surface, &rcDest);
    SDL_DestroySurface(textSurface);
}

void Canvas_draw_image(Canvas* pCanvas, Canvas* pImage, U16 x, U16 y) {

    U16 sx, sy;
    Transform_to_screen(&g_app.transform, x, y, &sx, &sy);
    SDL_Rect rcDest = { 0,0,0,0 };
    rcDest.x = sx;
    rcDest.y = sy;
    rcDest.w = pCanvas->surface[0].w;
    rcDest.h = pCanvas->surface[0].h;

    SDL_BlitSurface(pImage->surface, NULL, pCanvas->surface, &rcDest);

}

