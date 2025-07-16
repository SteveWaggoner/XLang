
#include "utils.h"

U16 djb2_hash(U8* bytes, U8 len, U16 prev_hash) {

    U8 i = 0;
    U16 hash = prev_hash;
    if (hash == 0) {
        hash = 5381;
    }
    while (i < len) {
        hash = ((hash << 5) + hash) + *bytes; /* hash * 33 + c */
        i++;
        bytes++;
    }
    return hash;
}


// https://github.com/edrosten/8bit_rng/blob/master/rng-4261412736.c
U8 random_byte() {
    static U8 x = 1, y = 0, z = 0, a = 1;

    U8 t = x ^ (x << 4);
    x = y;
    y = z;
    z = a;
    a = z ^ t ^ (z >> 1) ^ (t << 1);
    return a;
}