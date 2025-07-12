#ifndef SHAPE_API_H_
#define SHAPE_API_H_


#include "c6502.h"

typedef void (*PUT_PIXEL_FUNC)(void* canvasPtr, I16 x, I16 y);

typedef struct tagSHAPE_POINT {
    I16 x;
    I16 y;
} SHAPE_POINT;

#define MAX_POINTS 256

typedef struct tagSHAPE_CANVAS {
    U16 point_cnt;
    U16 max_point_cnt;
    SHAPE_POINT points[MAX_POINTS];
} SHAPE_CANVAS;

void putPixelInArray(void* canvasPtr, I16 x, I16 y);

typedef struct tagSHAPE_LINE {
    I16 y;
    I16 start_x;
    I16 end_x;
} SHAPE_LINE;

#define MAX_LINES 256


void Shape_filled_circle(I16 x, I16 y, I16 r, PUT_PIXEL_FUNC putPixelFunc, void* canvasPtr);
void Shape_circle(I16 x0, I16 y0, I16 radius, PUT_PIXEL_FUNC putPixelFunc, void* canvasPtr);
void Shape_line(I16 x0, I16 y0, I16 x1, I16 y1, PUT_PIXEL_FUNC putPixelFunc, void* canvasPtr);

void Shape_filled_octogon(I16 centerx, I16 centery, I16 radius, float slope_dx, float slope_dy, PUT_PIXEL_FUNC putPixelFunc, void* canvasPtr);
I16  Shape_get_octogon_lines(I16 width, I16 height, float slope_dx, float slope_dy, SHAPE_LINE* lines, I16 max_line_cnt);
void Shape_find_octogon_corner(U16 half_width, U16 half_height, float slope_dx, float slope_dy, SHAPE_POINT* pnt);
float Math_slope(SHAPE_POINT* P1, SHAPE_POINT* P2);
float Math_y_intercept(SHAPE_POINT* P1, float slope);
I8 Math_line_intersect(float m1, U16 b1, float m2, I16 b2, SHAPE_POINT* retPnt);
I8 Math_line_intersect_test(SHAPE_POINT* A1, SHAPE_POINT* A2, SHAPE_POINT* B1, SHAPE_POINT* B2);

#endif




