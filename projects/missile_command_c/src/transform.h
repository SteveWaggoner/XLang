#ifndef TRANSFORM_H_
#define TRANSFORM_H_

#include "c6502.h"

// Internal class for 2-D coordinate transformations
typedef struct tagTransform {
    U16 xbase;
    U16 ybase;
    U16 xscale;
    U16 yscale;
} Transform;

void Transform_init(Transform* pTransform, U16 w, U16 h, U16 xlow, U16 ylow, U16 xhigh, U16 yhigh);
void Transform_to_screen(Transform* pTransform, U16 x, U16 y, U16* pXs, U16* pYs);
void Transform_to_world(Transform* pTransform, U16 xs, U16 ys, U16* pX, U16* pY);

#endif