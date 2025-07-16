
#include "list.h"

#include <assert.h>

U8* List_allocItem(U8* pList, const U16 itemSize, const U16 numElements) {
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

void List_setAll(U8* pList, const U16 itemSize, const U16 numElements, const BOOLEAN active) {
    U16 i;
    assert(pList);
    for (i = 0; i < numElements; i++) {
        *pList = active;
        pList += itemSize;
    }
}

