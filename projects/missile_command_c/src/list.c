
#include "list.h"


#include <stdio.h>
#include <assert.h>

void Item_init(Item* pItem) {
    assert(pItem);
    pItem->active = FALSE;
}


void Item_free(Item* pItem) {
    assert(pItem);
    assert(pItem->pList);
    pItem->active = FALSE;
    pItem->pList->num_active--;
}


void List_init(List* pList, U8 item_size, U8 max_items, BOOLEAN active) {

    U8 i;

    assert(pList);
    assert(item_size>0);
    assert(max_items>0);

    pList->item_size = item_size;
    pList->max_items = max_items;

    if (active == TRUE) {
        pList->num_active = max_items;
    } else {
        pList->num_active = 0;
    }

    pList->next_alloc = 0;


    printf("List_init %p max_items=%d, sizeof(List) = %d, item_size = %d\n", pList, max_items, sizeof(List), item_size);

    for(i=0; i<max_items; i++) {
        Item* pItem = (Item*) (((U8*) pList) + sizeof(List) + (item_size * i));

        //Alarm_dump(pItem);

        pItem->pList = pList;
        pItem->active = active;

  //      Alarm_dump(pItem);
    }

}


Item* List_getItem(List* pList, U8 i) {
    Item* pItem;
    assert(pList);
    assert(pList->max_items > i);
    pItem = (Item*) (((U8*) pList) + sizeof(List) + (pList->item_size * i));

    //printf("List_getItem(pList=%p, i=%d) = %p\n", pList, i, pItem);

    return pItem;
}


Item* List_allocItem(List* pList) {

    U8 n;
    U8 i;
    Item* pItem;

    assert(pList);

    n = pList->next_alloc;
    i = 0;

    while (i < pList->max_items) {

        pItem = List_getItem(pList, n);

        if ( pItem->active == FALSE ) {

            Item_init(pItem);
            pItem->active = TRUE;
            pList->next_alloc = ( n + 1 ) % pList->max_items;
            pList->num_active++;
            return pItem;
        }

        i++;
        n = (n + 1) % pList->max_items;
    }

    printf("bad_alloc\n");
    return NULL;
}

void List_clear(List* pList) {
    U8 i;
    Item* pItem;
    assert(pList);
    pList->next_alloc = 0;
    for (i=0; i < pList->max_items; i++) {
        pItem = List_getItem(pList, i);
        if ( pItem->active ) {
            Item_free(pItem);
        }
    }
}

U16 djb2HashFunction(U8* bytes, U8 len, U16 prev_hash) {

    U8 i = 0;
    U16 hash = prev_hash;
    if ( hash == 0 ) {
        hash = 5381;
    }
    while ( i < len ) {
        hash = ((hash << 5) + hash) + *bytes; /* hash * 33 + c */
        i++;
        bytes++;
    }
    return hash;
}

U16 Item_getHash(Item* pItem, U16 prev_hash) {
    assert(pItem);
    assert(pItem->pList);
    return djb2HashFunction((U8*) pItem, pItem->pList->item_size, prev_hash);
}


U8 List_getCollisions(List* pList, List* pOtherList, COLLISION_FUNC has_collision_func, Hit hits[], U8 max_hits) {
    
    U8 h = 0;
    U8 i;
    U8 j;
    Item* pItem;
    Item* pOtherItem;

    assert(pList);
    assert(pOtherList);
    for (i=0; i<pList->max_items; i++) {
        pItem = List_getItem(pList, i);
        if ( pItem->active ) {
            for (j=0; j<pOtherList->max_items; j++) {
                pOtherItem = List_getItem(pOtherList, j);
                if ( pOtherItem->active && h < max_hits ) {
                    if ( has_collision_func(pItem, pOtherItem) ) {
                        hits[h].a = pItem;
                        hits[h].b = pOtherItem;
                        h++;
                    }
                }
            }
        }
    }
    return h;
}

U16 List_getHash(List* pList, U16 prev_hash) {
        
    U16 hash_val = prev_hash;
    U8 i;
    Item* pItem;
    for (i=0; i < pList->max_items; i++) {
        pItem = List_getItem(pList, i);
        if ( pItem->active ) {
            hash_val = Item_getHash(pItem, hash_val);
        }
    }
    return hash_val;
}

void List_dump(List* pList, ITEM_DUMP_FUNC dumpFunc) {
    
    U8 i;
    Item* pItem;

    assert(pList->item_size>0);
    assert(pList->max_items>0);

    printf("list %p, num_active=%d, max_items=%d, item_size=%d, next_alloc=%d\n", 
                pList, pList->num_active, pList->max_items, pList->item_size, pList->next_alloc);
    for (i=0; i < pList->max_items; i++) {
        pItem = List_getItem(pList, i);
        if ( pItem->active ) {
            printf("(%d) ", i);
            (*dumpFunc)(pItem);
            printf("\n");
        }
    }
}


/*
/// USAGE
*/


typedef struct {
    Item item;
    U8 foo;
} Alien;

void Alien_dump(Alien* alien) {
    printf("{foo=%d}", alien->foo);
}

U16 Alien_hash(Alien* alien) {
   assert(alien);
   return alien->foo;
}

BOOLEAN CollisionFunc (Item* pItem, Item* pOtherItem) {

    Alien* pAlien = (Alien*) pItem;
    Alien* pOtherAlien = (Alien*) pOtherItem;

    return pAlien->foo == pOtherAlien->foo;
}

typedef struct {
    List list;
    Alien alien[6];
} AlienList;

const int debug=123;

int xmain() {
    
    AlienList aliens;
    Alien* huh, *a, *b, *c;
    int hash=0, i;
    Hit hits[1];

    AlienList moreAliens;
    U8 hitCnt;

    INIT_LIST(Alien, aliens, FALSE);
    INIT_LIST(Alien, moreAliens, FALSE);

    a = ALLOC_ITEM(Alien, aliens);
    a->foo = 88;

    b = ALLOC_ITEM(Alien, aliens);
    b->foo = 99;

    c = ALLOC_ITEM(Alien, moreAliens);
    c->foo = 88;

    c = ALLOC_ITEM(Alien, moreAliens);
    c->foo = 88;

    c = ALLOC_ITEM(Alien, moreAliens);
    c->foo = 88;


    DUMP_LIST(Alien, aliens); 
    DUMP_LIST(Alien, moreAliens); 
    hitCnt = GET_COLLISIONS(aliens, moreAliens, CollisionFunc, hits);

    printf("hitCnt = %d\n", hitCnt);
    for(i=0; i<hitCnt; i++) {
        printf("%d a = %p  (%d)\n", i, hits[i].a, ((Alien*)hits[i].a)->foo);
        printf("%d b = %p  (%d)\n", i, hits[i].b, ((Alien*)hits[i].b)->foo);
    }

    FREE_ITEM(Alien,GET_ITEM(Alien,aliens,0)); 

    huh = ALLOC_ITEM(Alien, aliens);
    assert(huh);
    huh->foo = 39; 

    FREE_ITEM(Alien,huh);
    huh = ALLOC_ITEM(Alien, aliens);
    DUMP_LIST(Alien, aliens);
    DUMP_ITEM(Alien, huh);

    huh = ALLOC_ITEM(Alien, aliens);
    huh = ALLOC_ITEM(Alien, aliens);

    hash = HASH_LIST(Alien, aliens);
    printf("hash = %d\n", hash);

    DUMP_LIST(Alien, aliens);
    CLEAR_LIST(Alien, aliens);

    DUMP_LIST(Alien, aliens);

    hash = HASH_LIST(Alien, aliens);
    printf("hash = %d\n", hash);
}

