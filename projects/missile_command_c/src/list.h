#ifndef LIST_H_
#define LIST_H_

#include "c6502.h"

U8*  List_allocItem(U8* pList, const U16 itemSize, const U16 numElements);
void List_setAll(U8* pList, const U16 itemSize, const U16 numElements, const BOOLEAN active);

#define LIST_SIZE(CLASS,LIST) sizeof(LIST)/sizeof(CLASS)
#define ALLOC_ITEM(CLASS,LIST) ((CLASS*) List_allocItem((U8*)LIST,sizeof(CLASS), sizeof(LIST)/sizeof(CLASS)))
#define FREE_ITEM(VAR)  assert(VAR); ((BOOLEAN*)VAR)[0] = 0;
#define GET_ITEM(CLASS,LIST,INDEX)  &((CLASS*)LIST)[INDEX];
#define SET_ALL_INACTIVE(CLASS,LIST)  List_setAll((U8*)LIST,sizeof(CLASS), sizeof(LIST)/sizeof(CLASS),FALSE)
#define SET_ALL_ACTIVE(CLASS,LIST)  List_setAll((U8*)LIST,sizeof(CLASS), sizeof(LIST)/sizeof(CLASS),TRUE)

#endif 
