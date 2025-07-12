#include "shape.h"

#include <assert.h>

typedef void (*PUT_PIXEL_FUNC)(void* canvasPtr, U16 x, U16 y);

// https://stackoverflow.com/questions/1201200/fast-algorithm-for-drawing-filled-circles
void Shape_filled_circle(U16 x, U16 y, U16 r, PUT_PIXEL_FUNC putPixelFunc, void* canvasPtr) {
    I32 r2 = r * r;
    I32 area = r2 << 2;
    I32 rr = r << 1;
    I32 i;
    for (i = 0; i < area; i++) {
        I32 tx = (i % rr) - r;
        I32 ty = (i / rr) - r;
        if (tx * tx + ty * ty <= r2) {
            (*putPixelFunc)(canvasPtr, x + tx, y + ty);
        }
    }
}

void Shape_circle(U16 x0, U16 y0, U16 radius, PUT_PIXEL_FUNC putPixelFunc, void* canvasPtr) {
    I32 f = 1 - radius;
    I32 ddf_x = 1;
    I32 ddf_y = -2 * radius;
    I32 x = 0;
    I32 y = radius;
    (*putPixelFunc)(canvasPtr, x0, y0 + radius);
    (*putPixelFunc)(canvasPtr, x0, y0 - radius);
    (*putPixelFunc)(canvasPtr, x0 + radius, y0);
    (*putPixelFunc)(canvasPtr, x0 - radius, y0);

    while (x < y) {
        if (f >= 0) {
            y -= 1;
            ddf_y += 2;
            f += ddf_y;
        }
        x += 1;
        ddf_x += 2;
        f += ddf_x;
        (*putPixelFunc)(canvasPtr, x0 + x, y0 + y);
        (*putPixelFunc)(canvasPtr, x0 - x, y0 + y);
        (*putPixelFunc)(canvasPtr, x0 + x, y0 - y);
        (*putPixelFunc)(canvasPtr, x0 - x, y0 - y);
        (*putPixelFunc)(canvasPtr, x0 + y, y0 + x);
        (*putPixelFunc)(canvasPtr, x0 - y, y0 + x);
        (*putPixelFunc)(canvasPtr, x0 + y, y0 - x);
        (*putPixelFunc)(canvasPtr, x0 - y, y0 - x);
    }
}


void Shape_line(U16 x0, U16 y0, U16 x1, U16 y1, PUT_PIXEL_FUNC putPixelFunc, void* canvasPtr) {

    // Bresenham's algorithm
    I32 dx = abs(x1 - x0);
    I32 dy = abs(y1 - y0);
    I32 x = x0;
    I32 y = y0;
    I32 sx = (x0 > x1) ? -1 : 1;
    I32 sy = (y0 > y1) ? -1 : 1;
    I32 err = dx - dy;

    while (1) {
        (*putPixelFunc)(canvasPtr, x, y);
        if (x == x1 && y == y1) {
            break;
        }
        U32 e2 = 2 * err;
        if (e2 > -dy) {
            err -= dy;
            x += sx;
        }
        if (e2 < dx) {
            err += dx;
            y += sy;
        }
    }
}
    
void putPixelInArray(void* canvasPtr, U16 x, U16 y) {
    SHAPE_CANVAS* arrCanvas = canvasPtr; //hope it is this type
    assert(arrCanvas->max_point_cnt <= MAX_POINTS);
    assert(arrCanvas->point_cnt < MAX_POINTS);

    arrCanvas->points[arrCanvas->point_cnt].x = x;
    arrCanvas->points[arrCanvas->point_cnt].y = y;
    arrCanvas->point_cnt++;
}

void Shape_filled_octogon(U16 centerx, U16 centery, U16 radius, float slope_dx, float slope_dy, PUT_PIXEL_FUNC putPixelFunc, void* canvasPtr) {
    U16 width = radius * 2;
    U16 height = radius * 2;
    SHAPE_LINE lines[MAX_LINES];
    U16 line_cnt = Shape_get_octogon_lines(width, height, slope_dx, slope_dy, lines, MAX_LINES);
    U16 i;
    for (i = 0; i < line_cnt; i++) {
        U16 y = lines[i].y;
        U16 start_x = lines[i].start_x;
        U16 end_x = lines[i].end_x;
        
        I32 py = centery + y - radius;
        I32 x;
        for (x = start_x; x < end_x; x++) {
            I32 px = centerx + x - radius;
            (*putPixelFunc)(canvasPtr, px, py);
        }
    }
}

U16 Shape_get_octogon_lines(U16 width, U16 height, float slope_dx, float slope_dy, SHAPE_LINE* lines, U16 max_line_cnt) {

    U16 cornerx=0, cornery=0;
    Shape_find_octogon_corner(width / 2, height / 2, slope_dx, slope_dy, &cornerx, &cornery);

    SHAPE_CANVAS arrCanvas;
    arrCanvas.point_cnt = 0;
    arrCanvas.max_point_cnt = MAX_POINTS;
    Shape_line(width / 2, 0, cornerx, cornery, putPixelInArray, &arrCanvas);
    Shape_line(cornerx, cornery, 0, height / 2, putPixelInArray, &arrCanvas);

    assert(height <= max_line_cnt);
    U16 line_cnt = 0;
    U16 i;
    for (i = 0; i < height; i++) {
        lines[i].y = -1;
        lines[i].start_x = -1;
        lines[i].end_x = -1;
    }

    for (i = 0; i < arrCanvas.point_cnt;i++) {
        U16 x = arrCanvas.points[i].x;
        U16 y = arrCanvas.points[i].y;
        assert(y < max_line_cnt);
        lines[y].start_x = x;
        lines[y].end_x = width - x;

        lines[height - y - 1].start_x = x;
        lines[height - y - 1].end_x = width - x;
    }

    return arrCanvas.point_cnt;
}


void Shape_find_octogon_corner(U16 half_width, U16 half_height, float slope_dx, float slope_dy, SHAPE_POINT* pnt) {

    assert(pnt);

    if (slope_dx == slope_dy) {
        pnt->x = half_width / 2;
        pnt->y = half_height/2;
        return;
    }

    SHAPE_POINT A1 = { 0,0 };
    SHAPE_POINT B1 = { half_width, half_height };

    float slope_A = slope_dy / slope_dx;
    float slope_B = slope_dx / slope_dy;
    U16 y_int_A = Math_y_intercept(&A1, slope_A);
    U16 y_int_B = Math_y_intercept(&B1, slope_B);

    Math_line_intersect(slope_A, y_int_A, slope_B, y_int_B, pnt);

    // flip y
    pnt->y = half_height - pnt->y;
}


//  https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
float Math_slope(SHAPE_POINT* P1, SHAPE_POINT* P2) {
    // dy / dx
    // (y2 - y1) / (x2 - x1)
    return (P2->y - P1->y) / (P2->x - P1->x);
}

float Math_y_intercept(SHAPE_POINT* P1, float slope) {
    // y = mx + b
    // b = y - mx
    // b = P1[1] - slope * P1[0]
    return P1->y - slope * P1->x;
}

U8 Math_line_intersect(float m1, U16 b1, float m2, U16 b2, SHAPE_POINT* retPnt) {
    if (m1 == m2) {
        printf("These lines are parallel!!!\n");
        return 0;
    }
    // y = mx + b
    // Set both lines equal to find the intersection point in the x direction
    // m1 * x + b1 = m2 * x + b2
    // m1 * x - m2 * x = b2 - b1
    // x * (m1 - m2) = b2 - b1
    // x = (b2 - b1) / (m1 - m2)
    retPnt->x = (b2 - b1) / (m1 - m2);
    // Now solve for y -- use either line, because they are equal here
    // y = mx + b
    retPnt->y = m1 * retPnt->x + b1;

    return 1;
}

U8 Math_line_intersect_test(SHAPE_POINT* A1, SHAPE_POINT* A2, SHAPE_POINT* B1, SHAPE_POINT* B2) {
    float slope_A = Math_slope(A1, A2);
    float slope_B = Math_slope(B1, B2);
    U16   y_int_A = Math_y_intercept(A1, slope_A);
    U16   y_int_B = Math_y_intercept(B1, slope_B);
    SHAPE_POINT retPnt;
    return Math_line_intersect(slope_A, y_int_A, slope_B, y_int_B, &retPnt);
}



