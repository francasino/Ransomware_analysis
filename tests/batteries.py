from ent import readdata, entropy, pearsonchisquare
from fips import monobits, poker, run, longruns, contrun

import os


# Ent (John Walker) tests called from the module developed by RSmith
def ent(path):
    data, cnts = readdata(path)
    res_entropy = entropy(cnts)
    res_chi_score = pearsonchisquare(cnts)

    return res_entropy, res_chi_score


# FIPS140 tests, called from the appropriate module
def fips140(fn, ver, p):
    res = []
    c = []

    fs = os.stat(fn)

    with open(fn, 'rb') as seq:
        params = p

        if fs.st_size/(2500*params) < 1:
            params = int(fs.st_size/2500)

        for i in range(params):
            stat = []
            r = []

            s = seq.read(2500)

            rtmp, stattmp = monobits(s, ver)
            r.append(rtmp)
            stat.append(stattmp)

            rtmp, stattmp = poker(s, ver)
            r.append(rtmp)
            stat.append(stattmp)

            rtmp, stattmp = run(s, ver)
            r.append(rtmp)
            stat.append(stattmp)

            rtmp, stattmp = longruns(s, ver)
            r.append(rtmp)
            stat.append(stattmp)

            rtmp = contrun(s, ver)
            r.append(rtmp)

            res.append(r)
            c.append(stat)

    return res, c, params
