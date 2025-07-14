#ifndef LIST_H_
#define LIST_H_

#include "c6502.h"

#pragma pack(push,1)
typedef struct {
    U8 item_size;
    U8 max_items;
    U8 num_active;
    U8 next_alloc;
} List;

typedef struct {
    BOOLEAN active; 
    List* pList;
} Item;

typedef struct {
    Item* a;
    Item* b;
} Hit;
#pragma pack(pop)

typedef BOOLEAN (*COLLISION_FUNC)(Item* pItem, Item* pOtherItem);
typedef void (*ITEM_DUMP_FUNC)(Item* pItem);

void Item_init(Item* pItem);
void Item_free(Item* pItem);
U16  Item_getHash(Item* pItem, U16 prev_hash);

void  List_init(List* pList, U8 item_size, U8 max_items, BOOLEAN active);
Item* List_getItem(List* pList, U8 i);
Item* List_allocItem(List* pList);
void  List_clear(List* pList);
U8    List_getCollisions(List* pList, List* pOtherList, COLLISION_FUNC has_collision_func, Hit hits[], U8 max_hits);
U16   List_getHash(List* pList, U16 prev_hash);
void  List_dump(List* pList, ITEM_DUMP_FUNC dumpFunc);

U16   djb2HashFunction(U8* bytes, U8 len, U16 prev_hash);

#define INIT_LIST(CLASS,VAR,ACTIVE)  List_init((List*)& VAR, sizeof(CLASS), (sizeof(CLASS ## List) - sizeof(List)) / sizeof(CLASS), ACTIVE)
#define DUMP_LIST(CLASS,VAR)  List_dump((List*)& VAR, (ITEM_DUMP_FUNC) CLASS ## _dump)
#define CLEAR_LIST(CLASS,VAR) List_clear((List*)& VAR)
#define HASH_LIST(CLASS,VAR) List_getHash((List*)& VAR, 0)

#define GET_ITEM(CLASS,VAR,INDEX) (CLASS*) List_getItem((List*)& VAR,INDEX)
#define GET_COLLISIONS(LIST1,LIST2,FUNC,HITS)  List_getCollisions((List*)& LIST1, (List*)& LIST2, FUNC, HITS, sizeof(HITS)/sizeof(Hit))

#define ALLOC_ITEM(CLASS,VAR) (CLASS*) List_allocItem((List*)& VAR)
#define FREE_ITEM(CLASS,VAR)  Item_free((Item*) VAR)
#define DUMP_ITEM(CLASS,VAR)  CLASS ## _dump (VAR)

#endif 
