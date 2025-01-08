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

        if isinstance(val, int):
            if val < 0:
                raise Exception("value too small for byte ("+str(val)+")")
            elif val > 255:
                raise Exception("value too big for byte ("+str(val)+")")
            self.byte = val
        elif isinstance(val, bool):
            self.byte = val  # 0=FALSE, 1=TRUE ... leave a bool here so can trap math on bool
        else:
            raise Exception("value not integer (val="+str(val)+", type="+str(type(val))+")")


    def set(self, val):
        if isinstance(val,Byte):
            self.byte = val.byte
        else:
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

        if isinstance(self.byte,bool):
            raise "math on a boolean?!?"

        return Byte(self.byte + o_num)

    def __sub__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.byte

        if isinstance(self.byte,bool):
            raise "math on a boolean?!?"

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

        if isinstance(word, int):
            if word < -32768:
                raise Exception("value too small for word ("+str(word)+")")
            elif word > 32767:
                raise Exception("value too big for word ("+str(word)+")")
            self.word = word
        else:
            raise Exception("value not integer (word="+str(word)+", type="+str(type(word))+")")

    def set(self, val):
        if isinstance(val,Word):
            self.word = val.word
        else:
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

    def __sub__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.word

        return Word(self.word - o_num)

    def __mul__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.word

        return Word(int(self.word * o_num))

    def __truediv__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.word

        return Word(int(self.word / o_num))

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


# 32bit for val  (-2b to 2b)
class DWord:
    def __init__(self, dword=0):

        if isinstance(dword, int):
            if dword < -2000000000:
                raise Exception("value too small for word ("+str(dword)+")")
            elif dword > 2000000000:
                raise Exception("value too big for word ("+str(dword)+")")
            self.dword = dword
        else:
            raise Exception("value not integer ("+str(dword)+")")

    def set(self, val):
        if isinstance(val,DWord):
            self.dword = val.dword
        else:
            self.__init__(val)
        return self

    def get(self):
        return self.dword

    def __str__(self):
        return str(self.get())

    def __add__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.dword

        return DWord(self.dword + o_num)

    def __mod__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.dword

        return DWord(self.dword % o_num)

    def __gt__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.dword

        return self.dword > o_num

    def __lt__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.dword

        return self.dword < o_num

    def __eq__(self, o):
        if isinstance(o, int):
            o_num = o
        else:
            o_num = o.dword

        return self.dword == o_num




# 11bit for val, 5bits for decimal  (-1k to 1k)
class WordDecimal:
    def __init__(self, worddec=0):

        if isinstance(worddec,int):
            if worddec < -32768:
                raise Exception("value too small for word ("+str(worddec)+")")
            elif worddec > 32767:
                raise Exception("value too big for word ("+str(worddec)+")")
            self.worddec = worddec
        else:
            raise Exception("value not integer ("+str(worddec)+")")


    def set(self, val):
        if isinstance(val,WordDecimal):
            self.worddec = val.worddec
        else:
            self.__init__(int(val * 32))
        return self

    def get(self):
        return self.worddec / 32

    def abs(self):
        return WordDecimal(abs(self.worddec))

    def get_word(self):
        return Word(int(self.get()))

    def __str__(self):
        return str(self.get()) + " (word="+str(self.worddec)+")"

    def __add__(self, o):
        if isinstance(o, int):
            o_num = o * 32
        elif isinstance(o, Word):
            o_num = o.word * 32
        else:
            o_num = o.worddec
        return WordDecimal(self.worddec + o_num)

    def __sub__(self, o):
        if isinstance(o, int):
            o_num = o * 32
        else:
            o_num = o.worddec
        return WordDecimal(self.worddec - o_num)

    def __mul__(self, o):
        if isinstance(o, int):
            o_num = o * 32
        else:
            o_num = o.worddec

        return WordDecimal(int(self.worddec * o_num / 32))

    def __truediv__(self, o):
        if isinstance(o, int) or isinstance(o,float):
            o_num = o * 32
        elif isinstance(o, Word):
            o_num = o.word
        else:
            o_num = o.worddec

        return WordDecimal(int(32 * self.worddec / o_num))

    def __mod__(self, o):
        if isinstance(o, int):
            o_num = o * 32
        else:
            o_num = o.worddec

        return WordDecimal(self.worddec % o_num)

    def __gt__(self, o):
        if isinstance(o, int):
            o_num = o * 32
        else:
            o_num = o.worddec

        return self.worddec > o_num

    def __lt__(self, o):
        if isinstance(o, int):
            o_num = o * 32
        elif isinstance(o, Word):
            o_num = o.word * 32
        else:
            o_num = o.worddec

        return self.worddec < o_num

    def __eq__(self, o):
        if isinstance(o, int):
            o_num = o * 32
        else:
            o_num = o.worddec

        return self.worddec == o_num



# 22bit for val, 10bits for decimal  (-2m to 2m)
class DWordDecimal:
    def __init__(self, dworddec=0):

        if isinstance(dworddec,int):
            if dworddec < -2000000000:
                raise Exception("value too small for word ("+str(dworddec)+")")
            elif dworddec > 2000000000:
                raise Exception("value too big for word ("+str(dworddec)+")")
            self.dworddec = dworddec
        else:
            raise Exception("value not integer ("+str(dworddec)+")")

    def set(self, val):
        self.__init__(int(val * 1024))
        return self

    def get(self):
        return (self.dworddec / 1024)

    def abs(self):
        return DWordDecimal(abs(self.dworddec))

    def __str__(self):
        return str(self.get()) + " (dword="+str(self.dworddec)+")"

    def __add__(self, o):
        if isinstance(o, int):
            o_num = o * 1024
        else:
            o_num = o.dworddec

        return DWordDecimal(self.dworddec + o_num)

    def __mul__(self, o):
        if isinstance(o, int):
            o_num = o * 1024
        else:
            o_num = o.dworddec

        return DWordDecimal(int((self.dworddec * o_num) / 1024))

    def __truediv__(self, o):
        if isinstance(o, int) or isinstance(o,float):
            o_num = o * 1024
        else:
            o_num = o.dworddec

        return DWordDecimal(int(1024 * self.dworddec / o_num))

    def __mod__(self, o):
        if isinstance(o, int):
            o_num = o * 1024
        else:
            o_num = o.dworddec

        return DWordDecimal(self.dworddec % o_num)

    def __gt__(self, o):
        if isinstance(o, int):
            o_num = o * 1024
        else:
            o_num = o.dworddec

        return self.dworddec > o_num

    def __lt__(self, o):
        if isinstance(o, int):
            o_num = o * 1024
        else:
            o_num = o.dworddec

        return self.dword < o_num

    def __eq__(self, o):
        if isinstance(o, int):
            o_num = o * 1024
        else:
            o_num = o.dworddec

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

    dodo = Byte(False)
    print(dodo)
    dodo2 = Byte(True)
    print(dodo2)
    print(dodo + 1)


    hack = Byte().set(None)
    print(hack)


    foo = DWordDecimal().set(100000)
    print(foo)

    bar = WordDecimal().set(0.5)
    #bar2 = WordDecimal(bar)  # should fail
    #bar3 = WordDecimal(bar.get()) # should fail
    bar4 = WordDecimal().set(bar.get())
    bar5 = WordDecimal().set(bar)
    bar6 = WordDecimal().set(bar.word) # expect this to be wrong

    print(bar)
    print(bar4)
    print(bar5)
    print(bar6)

    sys.exit(1)

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




