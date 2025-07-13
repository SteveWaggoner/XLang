#include "transform.h"

void Transform_init(Transform* pTransform, I16 w, I16 h, I16 xlow, I16 ylow, I16 xhigh, I16 yhigh) {
    // w, h are width and height of window
    // (xlow,ylow) coordinates of lower-left [raw (0,h-1)]
    // (xhigh,yhigh) coordinates of upper-right [raw (w-1,0)]
    I16 xspan = (xhigh - xlow);
    I16 yspan = (yhigh - ylow);
    pTransform->xbase = xlow;
    pTransform->ybase = yhigh;
    pTransform->xscale = xspan / (w - 1);
    pTransform->yscale = yspan / (h - 1);
}

void Transform_to_screen(Transform* pTransform, I16 x, I16 y, I16* pXs, I16* pYs) {
    // Returns x, y in screen(actually window) coordinates
    I16 xs = (x - pTransform->xbase) / pTransform->xscale;
    I16 ys = (pTransform->ybase - y) / pTransform->yscale;

    *pXs = xs;
    *pYs = ys;
}

void Transform_to_world(Transform* pTransform, I16 xs, I16 ys, I16* pX, I16* pY) {
    // Returns xs, ys in world coordinates
    I16 x = xs * pTransform->xscale + pTransform->xbase;
    I16 y = pTransform->ybase - ys * pTransform->yscale;

    *pX = x;
    *pY = y;
}

void t_main() {

    Transform t;
    Transform_init(&t, 100, 100, 0, 0, 1000, 1000);

    U16 sx = 0, sy = 0, wx = 0, wy =0;
    Transform_to_screen(&t, 3, 3, &sx, &sy);
    Transform_to_world(&t, 3, 3, &wx, &wy);
}


