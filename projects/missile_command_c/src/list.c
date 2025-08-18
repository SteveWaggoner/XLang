
#include "list.h"

#include <assert.h>

U8* List_allocItem(U8* pList, const U8 itemSize, const U8 numElements) {
    U16 i;
    assert(pList);
    for (i = 0; i < numElements; i++) {
        if (*pList == 0) {
            *pList = 1;
            return pList;
        }
        pList += itemSize;
    }
    return NULL;
}

void List_setAll(U8* pList, const U8 itemSize, const U8 numElements, const BOOLEAN active) {
    U8 i;
    assert(pList);
    for (i = 0; i < numElements; i++) {
        *pList = active;
        pList += itemSize;
    }
}

U8 List_anyActive(U8* pList, const U8 itemSize, const U8 numElements) {
    U8 i;
    assert(pList);
    for (i = 0; i < numElements; i++) {
        if (*pList) {
            return i + 1;
        }
        pList += itemSize;
    }
    return 0;
}

U8 List_getRandom(U8* pList, const U8 itemSize, const U8 numElements) {
    U8 i;
    U8 choices[256] = { 0 };
    U8 choice_len = 0;
    assert(pList);
    for (i = 0; i < numElements; i++) {
        if (*pList) {
            choices[choice_len] = i;
            choice_len++;
        }
        pList += itemSize;
    }

    U8 random_choice = random_number(choice_len);
    return choices[random_choice];
}

U8 List_getActive(U8* pList, const U8 itemSize, const U8 numElements, U8** ptrs_buffer) {
    U8 i;
    U8 len = 0;
    assert(pList);
    for (i = 0; i < numElements; i++) {
        if (*pList) {
            ptrs_buffer[len] = pList;
            len++;
        }
        pList += itemSize;
    }
    return len;
}