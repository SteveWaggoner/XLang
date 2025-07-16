
#include "../graphics_api.h"
#include "../shape.h"

#include <stdio.h>
#include <assert.h>

void Canvas_init(Canvas* pCanvas, I16 width, U16 height) {
    assert(pCanvas);

    SDL_Surface* surface = SDL_CreateSurface(width, height, SDL_PIXELFORMAT_ARGB8888);
    assert(surface);
    pCanvas->surface = surface;
    pCanvas->pixels = surface->pixels;
    pCanvas->mode = 0;
    pCanvas->color = 0xfffff08f;
}

void Sprite_init(Sprite* pSprite, Canvas* canvas) {
    pSprite->active = FALSE;
    pSprite->canvas = canvas;
    pSprite->x = 0;
    pSprite->y = 0;
    pSprite->centerx = 0;
    pSprite->centery = 0;
}


App g_app;
void App_init(U8* title, U8 mode) {

    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO | SDL_INIT_JOYSTICK | SDL_INIT_EVENTS | SDL_INIT_SENSOR | SDL_INIT_GAMEPAD);
    TTF_Init();

    switch (mode)
    {
    case APP_MODE_SVGA:
    {
        g_app.width = 800;
        g_app.height = 600;
        g_app.scale_x = 1;
        g_app.scale_y = 1;
        break;
    }
    case APP_MODE_VGA:
    {
        g_app.width = 320;
        g_app.height = 200;
        g_app.scale_x = 4;
        g_app.scale_y = 4;
        break;
    }
    case APP_MODE_C64_MC:
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

    g_app.window = SDL_CreateWindow(title, g_app.width * g_app.scale_x, g_app.height * g_app.scale_y, 0);
    assert(g_app.window);
    g_app.renderer = SDL_CreateRenderer(g_app.window, NULL);
    assert(g_app.renderer);

    printf("RendererName = %s\n", SDL_GetRendererName(g_app.renderer));

    g_app.texture = NULL;
    g_app.has_key = 0;
    g_app.has_mouse_click = 0;

    Transform_init(&g_app.transform, g_app.width, g_app.height, 0, 200, 320, 0);

    SET_ALL_INACTIVE(Sprite, g_app.sprites);

    Canvas_init(&g_app.canvas,        g_app.width, g_app.height);
    Canvas_init(&g_app.canvas_merged, g_app.width, g_app.height);
}

void App_poll_events() {
    while (SDL_PollEvent(&g_app.event) != 0) {

        switch (g_app.event.type) {
        case SDL_EVENT_QUIT:
        {
            exit(0);
        }
        case SDL_EVENT_MOUSE_BUTTON_DOWN:
        {
            float mouseX, mouseY;
            SDL_GetMouseState(&mouseX, &mouseY);
            Transform_to_world(&g_app.transform, (I16) mouseX, (I16) mouseY, &g_app.last_mouse_click.x, &g_app.last_mouse_click.y);

            // for stretched canvas
            g_app.last_mouse_click.x = g_app.last_mouse_click.x / g_app.scale_x;
            g_app.last_mouse_click.y = g_app.last_mouse_click.y / g_app.scale_y;

            g_app.last_mouse_click.button = g_app.event.button.button;
            g_app.has_mouse_click = 1;
        }
        case SDL_EVENT_KEY_DOWN:
        {
            g_app.last_key = g_app.event.key.key;
            g_app.has_key = 1;
        }
        }
    }
}


void App_finish_draw() {
    if (g_app.texture != NULL) {
        SDL_DestroyTexture(g_app.texture);
    }

    Canvas_clear(&g_app.canvas_merged);
    Canvas_draw_image(&g_app.canvas_merged, &g_app.canvas, 0, 0);
        
    I16 i;
    for (i = 0; i < LIST_SIZE(Sprite, g_app.sprites); i++) {
        Sprite* sprite = &g_app.sprites[i];
        if (sprite->active) {
            Canvas_draw_image(&g_app.canvas_merged, sprite->canvas, sprite->x - sprite->centerx, sprite->y - sprite->centery);
        }
    }

    g_app.texture = SDL_CreateTextureFromSurface(g_app.renderer, g_app.canvas_merged.surface);
    SDL_SetTextureScaleMode(g_app.texture, SDL_SCALEMODE_NEAREST); //turn off fuzzy pixels
    SDL_RenderTexture(g_app.renderer, g_app.texture, NULL, NULL);
    SDL_RenderPresent(g_app.renderer);
}

Canvas* App_canvas() {
    return &g_app.canvas;
}

Sprite* App_sprite(U16 width, U16 height) {
    Sprite* sprite = ALLOC_ITEM(Sprite, g_app.sprites);

    Canvas* canvas = malloc(sizeof(Canvas)); //memory leak!
    Canvas_init(canvas, width, height);
    Sprite_init(sprite, canvas);
    sprite->active = TRUE;

    void* huh0 = &g_app.sprites;
    void* huh1 = GET_ITEM(Sprite, g_app.sprites, 0);
    int huhsize = sizeof(g_app.sprites);
    Sprite* huh = &g_app.sprites[0];

    return sprite;
}


I16 App_check_key() {
    if (g_app.has_key) {
        g_app.has_key = 0;
        return g_app.last_key;
    } else {
        return 0;
    }
}

MouseClick* App_check_mouse() {
    if (g_app.has_mouse_click) {
        g_app.has_mouse_click = 0;
        return &g_app.last_mouse_click;
    }
    else {
        return 0;
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
    if (pRect) {
        SDL_Rect rect = { pRect->x, pRect->y, pRect->w, pRect->h }; //typecast generic Rect to SDL_Rect
        SDL_FillSurfaceRect(pCanvas->surface, &rect, color);
    }
    else {
        SDL_FillSurfaceRect(pCanvas->surface, NULL, color);
    }
}


void Canvas_set_color(Canvas* pCanvas, U32 color, U8 mode) {
    pCanvas->color = color;
    pCanvas->mode = mode;
}

void Canvas_put_pixel(Canvas* pCanvas, I16 x, I16 y) {

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


void Canvas_draw_pixel(Canvas* pCanvas, I16 x, I16 y) {
    I16 sx, sy;
    Transform_to_screen(&g_app.transform, x, y, &sx, &sy);
    Canvas_put_pixel(pCanvas, sx, sy);
}


void Canvas_draw_line(Canvas* canvas, I16 x1, I16 y1, I16 x2, I16 y2) {
    I16 sx1, sy1, sx2, sy2;
    Transform_to_screen(&g_app.transform, x1, y1, &sx1, &sy1);
    Transform_to_screen(&g_app.transform, x2, y2, &sx2, &sy2);
    Shape_line(sx1, sy1, sx2, sy2, Canvas_put_pixel, canvas);
}

void Canvas_draw_filled_circle(Canvas* canvas, I16 x, I16 y, I16 radius) {
    I16 sx, sy;
    Transform_to_screen(&g_app.transform, x, y, &sx, &sy);
    Shape_filled_circle(sx, sy, radius, Canvas_put_pixel, canvas);
}

void Canvas_draw_filled_octogon(Canvas* canvas, I16 x, I16 y, I16 radius, float slope_dx, float slope_dy) {
    I16 sx, sy;
    Transform_to_screen(&g_app.transform, x, y, &sx, &sy);
    Shape_filled_octogon(sx, sy, radius, slope_dx, slope_dy, Canvas_put_pixel, canvas);
}

void Canvas_draw_circle(Canvas* canvas, I16 x, I16 y, I16  radius) {
    I16 sx, sy;
    Transform_to_screen(&g_app.transform, x, y, &sx, &sy);
    Shape_circle(sx, sy, radius, Canvas_put_pixel, canvas);
}

void Canvas_draw_rectangle(Canvas* canvas, I16 x1, I16 y1, I16 x2, I16 y2) {
    I16 sx1, sy1, sx2, sy2;
    Transform_to_screen(&g_app.transform, x1, y1, &sx1, &sy1);
    Transform_to_screen(&g_app.transform, x2, y2, &sx2, &sy2);

    Shape_line(sx1, sy1, sx1, sy2, Canvas_put_pixel, canvas);
    Shape_line(sx1, sy1, sx2, sy1, Canvas_put_pixel, canvas);
    Shape_line(sx2, sy1, sx2, sy2, Canvas_put_pixel, canvas);
    Shape_line(sx1, sy2, sx2, sy2, Canvas_put_pixel, canvas);
}

void Canvas_draw_text(Canvas* pCanvas, I16 x, I16 y, U8* text) {

    if (!g_app.font) {
        g_app.font = TTF_OpenFont("fonts/ARCADE_R.TTF", 8);
        if (!g_app.font) {
            printf("TTF_OpenFont() error = %s\n", SDL_GetError());
            return;
        }
    }

    // Create surface with rendered text
    SDL_Color textColor = { 0,0,0,0 };
    textColor.r = 100;
    textColor.g = 110;
    textColor.b = 160;

    SDL_Surface* textSurface = TTF_RenderText_Solid(g_app.font, text, strlen(text), textColor);
    assert(textSurface);

    U16 sx=0, sy=0;
    Transform_to_screen(&g_app.transform, x, y, &sx, &sy);

    SDL_Rect rcDest = { 0,0,0,0 };
    rcDest.x = sx;
    rcDest.y = sy;
    rcDest.w = textSurface->w;
    rcDest.h = textSurface->h;

    SDL_BlitSurface(textSurface, NULL, pCanvas->surface, &rcDest);
    SDL_DestroySurface(textSurface);
}

void Canvas_draw_image(Canvas* pCanvas, Canvas* pImage, I16 x, I16 y) {

    I16 sx, sy;
    Transform_to_screen(&g_app.transform, x, y, &sx, &sy);
    SDL_Rect rcDest = { 0,0,0,0 };
    rcDest.x = sx;
    rcDest.y = sy;
    rcDest.w = pCanvas->surface[0].w;
    rcDest.h = pCanvas->surface[0].h;

    SDL_BlitSurface(pImage->surface, NULL, pCanvas->surface, &rcDest);
}

