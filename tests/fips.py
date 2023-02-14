from numpy import *
from bitstring import BitArray

#monobits test as defined in FIPS140-1
def monobits(s, v):
    res = True
    chkvals = []
    b = BitArray(s)
    c = b.count(True)

    if v == 1:
        chkvals = [9654, 10346]
    elif v == 2:
        chkvals = [9725, 10275]

    if c <chkvals[0] or c>chkvals[1]:
        res = False

    return res, c


# poker test as defined in FIPS140-1
def poker(s, v):
    res = True
    chkvals = []

    if v == 1:
        chkvals = [1.03, 57.4]
    elif v == 2:
        chkvals = [2.16, 46.17]

    b = [0] * 16
    h = ''.join(format(x, '02x') for x in s)
    for i in h:
        b[int(i, 16)] = b[int(i, 16)] + 1

    sres = [x ** 2 for x in b]
    tres = sum(sres)
    fres = (16 / 5000) * tres - 5000

    if fres<chkvals[0] or fres>chkvals[1]:
        res = False

    return res, fres


# runs test as defined in FIPS140-1
def run(s, v):
    res = True
    chkval = []
    b = BitArray(s)
    c = [0] * 6
    cnt = 0

    if v == 1:
        chkval = [2267, 2733, 1079, 1421, 502, 748, 223, 402, 90, 223]
    elif v == 2:
        chkval = [2343, 2657, 1135, 1365, 542, 708, 251, 373, 111, 201]

    for i in range(0, len(b) - 1):
        if b[i] == b[i + 1]:
            cnt = cnt + 1
        else:
            if cnt < 6 and cnt > 0:
                c[cnt - 1] = c[cnt - 1] + 1
            elif cnt >= 6:
                c[5] = c[5] + 1
            cnt = 0

    if c[0] < chkval[0] or c[0] > chkval[1]:
        # print(x)
        res = False
    elif c[1] < chkval[2] or c[1] > chkval[3]:
        # print(x)
        res = False
    elif c[2] < chkval[4] or c[2] > chkval[5]:
        # print(x)
        res = False
    elif c[3] < chkval[6] or c[3] > chkval[7]:
        # print(x)
        res = False
    elif c[4] < chkval[8] or c[4] > chkval[9]:
        # print(x)
        res = False
    elif c[5] < chkval[8] or c[5] > chkval[9]:
        # print(x)
        res = False

    return res, c


# long run test as defined in FIPS140-1	- self evaluates
def longruns(s, v):
    res = True
    b = BitArray(s)
    c = [0, 0]
    chkval = 0

    if v == 1:
        chkval = 34
    elif v == 2:
        chkval = 26

    for i in b:
        # print(i)
        if i is False:
            c[1] = 0
            c[0] = c[0] + 1
            if c[0] > chkval:
                res = False
                break
        elif i is True:
            c[0] = 0
            c[1] = c[1] + 1
            if c[1] > chkval:
                res = False
                break

    return res, c


# continuous run test - checks for any repeated 16 byte sequence in the input sequence - repetition == failure
def contrun(s, v):
    res = True
    check = s[:16]
    comp = s[16:]

    for i in range(int(len(comp)/16)):
        chunk = comp[i*16:(i*32)]
        if chunk == check:
            res = False

    return res