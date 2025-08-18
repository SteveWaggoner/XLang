#ifndef UTILS_H_
#define UTILS_H_

#include "c6502.h"

U16 djb2_hash(U8* bytes, U8 len, U16 prev_hash);


U8 random_number(U8 max);
void random_seed(U8* pSeed);
U8 random_byte();

#endif
