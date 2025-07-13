#ifndef TRANSFORM_H_
#define TRANSFORM_H_

#include "c6502.h"

// Internal class for 2-D coordinate transformations
typedef struct tagTransform {
    I16 xbase;
    I16 ybase;
    I16 xscale;
    I16 yscale;
} Transform;

void Transform_init(Transform* pTransform, I16 w, I16 h, I16 xlow, I16 ylow, I16 xhigh, I16 yhigh);
void Transform_to_screen(Transform* pTransform, I16 x, I16 y, I16* pXs, I16* pYs);
void Transform_to_world(Transform* pTransform, I16 xs, I16 ys, I16* pX, I16* pY);

#endif