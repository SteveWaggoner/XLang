#!/usr/bin/python3.9

import sys


#
# purpose of these is to mimic C structures in Python to see
# if the logic works within the numeric ranges of the data types
#

#
# Byte is for tiny counters that shouldn't go out of range
#

#
# Word is for like screen size that is more than 256
#

#
# WordDecimal is a tiny decimal for vectors
#

#
# DWordDecimal is like a float to 3 decimal places
#


class Byte:
    def __init__(self, val=0):
        if val < 0:
            raise Exception("value too small for byte ("+str(val)+")")
        elif val > 255:
            raise Exception("value too big for byte ("+str(val)+")")
        elif not isinstance(val, int):
            raise Exception("value not integer ("+str(val)+")")

        self.byte = val

    def set(self, val):
        self.__init__(val)
        return self

    def get(self):
        return self.byte

    def __str__(self):
        return str(self.get())

    def __add__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.byte

        return Byte(self.byte + o_num)

    def __sub__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.byte

        return Byte(self.byte - o_num)


    def __mod__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.byte

        return Byte(self.byte % o_num)

    def __gt__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.byte

        return self.byte > o_num

    def __lt__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.byte

        return self.byte < o_num

    def __eq__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.byte

        return self.byte == o_num


# 16bit for val  (-32k to 32k)
class Word:
    def __init__(self, word=0):
        if word < -32768:
            raise Exception("value too small for word ("+str(word)+")")
        elif word > 32767:
            raise Exception("value too big for word ("+str(word)+")")
        elif not isinstance(word, int):
            raise Exception("value not integer ("+str(word)+")")

        self.word = word

    def set(self, val):
        self.__init__(val)
        return self

    def get(self):
        return self.word

    def __str__(self):
        return str(self.get())

    def __add__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.word

        return Word(self.word + o_num)

    def __mod__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.word

        return Word(self.word % o_num)

    def __gt__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.word

        return self.word > o_num

    def __lt__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.word

        return self.word < o_num

    def __eq__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.word

        return self.word == o_num



# 11bit for val, 5bits for decimal  (-1k to 1k)
class WordDecimal:
    def __init__(self, word=0):
        if word < -32768:
            raise Exception("value too small for word ("+str(word)+")")
        elif word > 32767:
            raise Exception("value too big for word ("+str(word)+")")
        elif not isinstance(word, int):
            raise Exception("value not integer ("+str(word)+")")

        self.word = word

    def set(self, val):
        self.__init__(int(val * 32))
        return self

    def get(self):
        return self.word / 32

    def abs(self):
        return WordDecimal(abs(self.word))

    def __str__(self):
        return str(self.get())

    def __add__(self, o):
        if isinstance(o, int):
            o_num = o * 32
        else:
            o_num = o.word

        return WordDecimal(self.word + o_num)

    def __mul__(self, o):
        if isinstance(o, int):
            o_num = o * 32
        else:
            o_num = o.word

        return WordDecimal(int(self.word * o_num / 32))

    def __truediv__(self, o):
        if isinstance(o, int) or isinstance(o,float):
            o_num = o * 32
        else:
            o_num = o.word

        return WordDecimal(int(32 * self.word / o_num))

    def __mod__(self, o):
        if isinstance(o, int):
            o_num = o * 32
        else:
            o_num = o.word

        return WordDecimal(self.word % o_num)

    def __gt__(self, o):
        if isinstance(o, int):
            o_num = o * 32
        else:
            o_num = o.word

        return self.word > o_num

    def __lt__(self, o):
        if isinstance(o, int):
            o_num = o * 32
        else:
            o_num = o.word

        return self.word < o_num

    def __eq__(self, o):
        if isinstance(o, int):
            o_num = o * 32
        else:
            o_num = o.word

        return self.word == o_num



# 22bit for val, 10bits for decimal  (-2m to 2m)
class DWordDecimal:
    def __init__(self, dword=0):
        if dword < -2000000000:
            raise Exception("value too small for dword ("+str(dword)+")")
        elif dword > 2000000000:
            raise Exception("value too big for dword ("+str(dword)+")")
        elif not isinstance(dword, int):
            raise Exception("value not integer ("+str(dword)+")")

        self.dword = dword

    def set(self, val):
        self.__init__(int(val * 1024))
        return self

    def get(self):
        return (self.dword / 1024)

    def abs(self):
        return DWordDecimal(abs(self.dword))

    def __str__(self):
        return str(self.get()) + " (dword="+str(self.dword)+")"

    def __add__(self, o):
        if isinstance(o, int):
            o_num = o * 1024
        else:
            o_num = o.dword

        return DWordDecimal(self.dword + o_num)

    def __mul__(self, o):
        if isinstance(o, int):
            o_num = o * 1024
        else:
            o_num = o.dword

        return DWordDecimal(int((self.dword * o_num) / 1024))

    def __truediv__(self, o):
        if isinstance(o, int) or isinstance(o,float):
            o_num = o * 1024
        else:
            o_num = o.dword

        return DWordDecimal(int(1024 * self.dword / o_num))

    def __mod__(self, o):
        if isinstance(o, int):
            o_num = o * 1024
        else:
            o_num = o.dword

        return DWordDecimal(self.dword % o_num)

    def __gt__(self, o):
        if isinstance(o, int):
            o_num = o * 1024
        else:
            o_num = o.dword

        return self.dword > o_num

    def __lt__(self, o):
        if isinstance(o, int):
            o_num = o * 1024
        else:
            o_num = o.dword

        return self.dword < o_num

    def __eq__(self, o):
        if isinstance(o, int):
            o_num = o * 1024
        else:
            o_num = o.dword

        return self.dword == o_num


# for testing... adjustable precision loss
class WordFloat:

    def __init__(self, val=0):
        PRECISION=3
        self.val = round(val,PRECISION)

    def set(self, val):
        self.__init__(val)
        return self

    def get(self):
        return self.val

    def abs(self):
        return WordFloat(abs(self.val))

    def __str__(self):
        return str(round(self.get(),8))

    def __add__(self, o):
        if isinstance(o, int) or isinstance(o,float):
            o_num = o
        else:
            o_num = o.val

        return WordFloat(self.val + o_num)

    def __mul__(self, o):
        if isinstance(o, int) or isinstance(o,float):
            o_num = o
        else:
            o_num = o.val

        return WordFloat(self.val * o_num)

    def __truediv__(self, o):
        if isinstance(o, int) or isinstance(o,float):
            o_num = o
        else:
            o_num = o.val

        return WordFloat(self.val / o_num)

    def __mod__(self, o):
        if isinstance(o, int) or isinstance(o,float):
            o_num = o
        else:
            o_num = o.val

        return WordFloat(self.val % o_num)

    def __gt__(self, o):
        if isinstance(o, int) or isinstance(o,float):
            o_num = o
        else:
            o_num = o.val

        return self.val > o_num

    def __lt__(self, o):
        if isinstance(o, int) or isinstance(o,float):
            o_num = o
        else:
            o_num = o.val

        return self.val < o_num

    def __eq__(self, o):
        if isinstance(o, int) or isinstance(o,float):
            o_num = o
        else:
            o_num = o.val

        return self.val == o_num


def main():

    foo = DWordDecimal().set(100000)
    print(foo)

    blah = WordDecimal().set(13.5)
    blah2 = blah % 20
    print(blah)
    print(blah2)

    huh = WordDecimal().set(0.22)
    huh2 = huh + huh + huh + huh + huh
    huh3 = huh * 5

    print(huh)
    print(huh2)
    print(huh3)

    ack = WordFloat().set(0.22)
    ack2 = ack + ack + ack + ack + ack
    ack3 = ack * 5

    print(ack)
    print(ack2)
    print(ack3)

    sys.exit(1)


if __name__=="__main__":
    main()




