from numpy import *
from bitstring import BitArray
import pandas as pd
import collections


# disjointedness test (return True if pass, False if fail)
def test0(s):
    a = []
    c = 0
    for i in range(1, 65536, 6):
        a.append(s[i:i + 6])

    a = sorted(a)

    for i in range(0, len(a) - 1):
        if a[i] == a[i + 1]:
            c += 1

    return c


# auto-correlation test
# this test needs rewriting - sourcem aterial was incorrect
def test5(s):
    t = []
    b = BitArray(s)

    for i in range(1, 5001):
        for j in range(1, 5001):
            temp = b[j] ^ b[j + i]
        t.append(temp)

    return sum(t)


# uniform distribution test (multinomial test variant)
def test6a(s):
    b = BitArray(s)
    c = 0
    L = 100000

    for i in range(0, L):
        if b[i] == 1:
            c = c + 1

    return c


# homogeneity test variants (6b, 7a, and 7b)
def test7(s):
    res = True
    b = BitArray(s)
    w2 = [[] for i in range(2)]
    w3 = [[] for i in range(4)]
    w4 = [[] for i in range(8)]
    stats = []
    n = 100000
    cnt = 0

    for k in [2, 3, 4]:
        f = 0
        b = b[cnt:]
        for i in range(cnt, len(b), k):
            temp = b[i:i + k]

            if k == 2:
                if temp[0] is False:
                    w2[0].append(temp)
                elif temp[0] is True:
                    w2[1].append(temp)

                if min([len(x) for x in w2]) >= n:
                    break
                elif max([len(x) for x in w2]) >= 10 * n and min([len(x) for x in w2]) == 0:
                    print("Deadman counter exceeded, test failed.")
                    return stats, res, int(cnt / 8)

            if k == 3:
                if temp[0] is False and temp[1] is False:
                    w3[0].append(temp)
                elif temp[0] is True and temp[1] is False:
                    w3[1].append(temp)
                elif temp[0] is False and temp[1] is True:
                    w3[2].append(temp)
                elif temp[0] is True and temp[1] is True:
                    w3[3].append(temp)

                if min([len(x) for x in w3]) >= n:
                    break
                elif max([len(x) for x in w3]) >= 10 * n and min([len(x) for x in w3]) == 0:
                    print("Deadman counter exceeded, test failed.")
                    return stats, res, int(cnt / 8)

            if k == 4:
                if temp[0] is False and temp[1] is False and temp[2] is False:
                    w4[0].append(temp)
                elif temp[0] is True and temp[1] is False and temp[2] is False:
                    w4[1].append(temp)
                elif temp[0] is False and temp[1] is True and temp[2] is False:
                    w4[2].append(temp)
                elif temp[0] is True and temp[1] is True and temp[2] is False:
                    w4[3].append(temp)
                elif temp[0] is False and temp[1] is False and temp[2] is True:
                    w4[4].append(temp)
                elif temp[0] is True and temp[1] is False and temp[2] is True:
                    w4[5].append(temp)
                elif temp[0] is False and temp[1] is True and temp[2] is True:
                    w4[6].append(temp)
                elif temp[0] is True and temp[1] is True and temp[2] is True:
                    w4[7].append(temp)

                if min([len(x) for x in w4]) >= n:
                    break
                elif max([len(x) for x in w4]) >= 10 * n and min([len(x) for x in w4]) == 0:
                    print("Deadman counter exceeded, test failed.")
                    return stats, int(cnt / 8)

            cnt += k

        if k == 2:
            tmp = []
            probs = []

            for i in range(len(w2)):
                tmp.append([str(j) for j in w2[i]])

            for i in range(len(tmp)):
                freq, M = transmat(tmp[i][:n])
                probs.append(M)

            stats.append(float(probs[0]['1']) + float(probs[1]['0']) - 1)

        if k == 3:
            tmp = []
            freq = []
            probs = []

            for i in range(len(w3)):
                tmp.append([str(j) for j in w3[i]])

            for i in range(len(tmp)):
                f, M = transmat([str(j) for j in w3[i][:n]])
                freq.append(f)
                probs.append(M)

            T = [0] * 2

            T[0] = T7([freq[0], freq[1]], n)
            T[1] = T7([freq[2], freq[3]], n)

            for i in T:
                stats.append(i)

        if k == 4:
            tmp = []
            freq = []
            probs = []

            for i in range(len(w4)):
                tmp.append([str(j.bin) for j in w4[i]])

            for i in range(len(tmp)):
                f, M = transmat([str(j.bin) for j in w4[i][:n]])
                freq.append(f)
                probs.append(M)

            T = [0] * 4

            T[0] = T7([freq[0], freq[4]], n)
            T[1] = T7([freq[1], freq[5]], n)
            T[2] = T7([freq[2], freq[6]], n)
            T[3] = T7([freq[3], freq[7]], n)

            for i in T:
                stats.append(i)

    return stats, int(cnt / 8)


def transmat(a):
    matrix = pd.Series(collections.Counter(map(tuple, a))).unstack().fillna(0)
    return matrix, (matrix.divide(matrix.sum(axis=1), axis=0))


def T7(f, n):
    p = [0, 0]

    # calculate probabilities for vemp
    for i in range(len(p)):
        f_i = 0
        for j in f:
            f_i += j.iloc[0, i]
        p[i] = f_i / (2 * n)

    T = 0
    for i in f:
        for t in range(len(p)):
            T += (i.iloc[0, t] - (n * p[t])) ** 2 / (n * p[t])

    return T


# Jean Sebastien Coron's entropy estimation test
# Code adapted from page 10 of http://www.crypto-uni.lu/jscoron/publications/entropy.pdf
def test8(s):
    Q = 2560
    K = 256000
    L = 8

    V = (1 << L)
    tab = [0] * V
    sum = 0

    for n in range(1, Q + 1):
        tab[int(s[n])] = n

    for n in range(Q + 1, Q + K + 1):
        k = s[n]
        sum += fcoef(n - tab[k])
        tab[k] = n

    fn = sum / K

    return fn


def fcoef(i):
    l = log(2)
    s = 0
    C = -0.8327462
    j = i - 1
    limit = 23

    if i < limit:
        for k in range(1, i):
            s += (1 / k)
        return s / l
    else:
        return log(j) / l - C + (1 / (2 * j) - 1 / (12 * (j ** 2))) / l