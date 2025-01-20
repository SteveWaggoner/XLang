#!/usr/bin/python3.9

from c6502 import Byte


class Item:
    def __init__(self):
        super().__init__()

        # memory allocation
        self.active = Byte(False)

    def destroy(self):
        if self.active:
            self.list.num_active = self.list.num_active - 1
            self.active = False



#
# fixed memory dynamic array (c) 2025 wagtech baby
#

class List:

    def __init__(self, item_class, max_items, active=0):

        self.num_active = Byte(0)
        self.next_alloc = Byte(0)
        self.items = []
        for x in range(max_items):
            i = item_class()
            i.list = self
            i.active = active
            self.items.append(i)

    def __getitem__(self, key):
        return self.items[key]

    def create(self):

        n = self.next_alloc.get()
        i = 0

        while i < len(self.items):
            if self.items[n].active == False:
                self.items[n].active = True
                self.next_alloc.set( ( n + 1 ) % len(self.items) )
                self.num_active.set( self.num_active + 1 )
                print("created "+str(self.items[n].__class__.__name__)+" "+str(n))
                return self.items[n]
            i = i + 1
            n = (n + 1) % len(self.items)

        print(self)
        raise Exception("bad alloc")


    def clear(self):
        for i in self.items:
            i.destroy()

    def get_collisions(self, other, has_collision_function):
        hits = []
        for a in self.items:
            if a.active:
                for b in other.items:
                    if b.active:
                        if has_collision_function(a,b):
                            hits.append((a,b))
        return hits


def main():
    my_list = List(Item,6)

    huh = my_list.create()
    huh = my_list.create()
    huh = my_list.create()
    huh = my_list.create()
    huh = my_list.create()
    print(my_list.num_active)

    huh.destroy()
    print(my_list.num_active)



if __name__=="__main__":
    main()


