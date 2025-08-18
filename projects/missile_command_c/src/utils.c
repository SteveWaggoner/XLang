
#include "utils.h"

#include <assert.h>

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


U8 rng_x = 1, rng_y = 0, rng_z = 0, rng_a = 1;

void random_seed(U8* pSeed) {
    assert(pSeed);
    rng_x = *pSeed++;
    rng_y = *pSeed++;
    rng_z = *pSeed++;
    rng_a = *pSeed++;
}

// 0 to max-1
U8 random_number(U8 max) {
    return random_byte() % max;
}

// https://github.com/edrosten/8bit_rng/blob/master/rng-4261412736.c
U8 random_byte() {
    U8 t = rng_x ^ (rng_x << 4);
    rng_x = rng_y;
    rng_y = rng_z;
    rng_z = rng_a;
    rng_a = rng_z ^ t ^ (rng_z >> 1) ^ (t << 1);
    return rng_a;
}