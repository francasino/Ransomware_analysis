#!/usr/bin/env python3
# file: ent.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2012-08-25T23:37:50+0200
# Last modified: 2018-07-08T13:37:52+0200
"""
Partial implementation of the ‘ent’ program by John "Random" Walker in Python.

See http://www.fourmilab.ch/random/ for the original.
"""

from __future__ import division, print_function
import argparse
import math
import sys
import numpy as np

__version__ = '0.7'
PI = 3.14159265358979323846


def main(argv):
    """
    Calculate and print figures about the randomness of the input files.

    Arguments:
        argv: Program options.
    """
    opts = argparse.ArgumentParser(prog='ent', description=__doc__)
    opts.add_argument(
        '-c', action='store_true', help="print occurrence counts (not implemented yet)"
    )
    opts.add_argument('-t', action='store_true', help="terse output in CSV format")
    opts.add_argument('-v', '--version', action='version', version=__version__)
    opts.add_argument("files", metavar='file', nargs='*', help="one or more files to process")
    args = opts.parse_args(argv)
    for fname in args.files:
        data, cnts = readdata(fname)
        e = entropy(cnts)
        c = pearsonchisquare(cnts)
        if args.t:
            terseout(data, e, c)
        else:
            textout(data, e, c)


def terseout(data, e, chi2):
    """
    Print the results in terse CSV.

    Arguments:
        data: file contents
        e: Entropy of the data in bits per byte.
        chi2: Χ² value for the data.
        p: Probability of normal z value.
        d: Percent distance of p from centre.
        scc: Serial correlation coefficient.
        mc: Monte Carlo approximation of π.
    """
    print('0,File-bytes,Entropy,Chi-square')
    print(f'1,{n},{e:.6f},{chi2:.6f}')


def textout(data, e, chi2):
    """
    Print the results in plain text.

    Arguments:
        data: file contents
        e: Entropy of the data in bits per byte.
        chi2: Χ² value for the data.
        p: Probability of normal z value.
        d: Percent distance of p from centre.
        scc: Serial correlation coefficient.
        mc: Monte Carlo approximation of π.
    """


def readdata(name):
    """
    Read the data from a file and count byte occurences.

    Arguments:
        name: Path of the file to read

    Returns:
        data: numpy array containing the byte values.
        cnts: numpy array containing the occurance of each byte.
    """
    data = np.fromfile(name, np.ubyte)
    cnts = np.bincount(data)
    return data, cnts


def entropy(counts):
    """
    Calculate the entropy of the data represented by the counts array.

    Arguments:
        counts: numpy array of counts for all byte values.

    Returns:
        Entropy in bits per byte.
    """
    counts = np.trim_zeros(np.sort(counts))
    sz = sum(counts)
    p = counts / sz
    ent = -sum(p * np.log(p) / math.log(256))
    return ent * 8


def pearsonchisquare(counts):
    """
    Calculate Pearson's χ² (chi square) test for an array of bytes.

    See [http://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test
    #Discrete_uniform_distribution]

    Arguments:
        counts: Numpy array of counts.

    Returns:
        χ² value
    """
    np = sum(counts) / 256
    return sum((counts - np)**2 / np)


if __name__ == '__main__':
    main(sys.argv[1:])
