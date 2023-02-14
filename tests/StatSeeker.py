#!/usr/bin/env python3
import argparse
import os
from batteries import ent, fips140
from utilities import dir_path, init_csv, ent_csv, fips_csv, sp80022_csv, file_info, csv_merge, corrs_csv, sq_csv
from subprocess import Popen, PIPE
from numpy import *
from bitstring import BitArray
from scipy.stats import power_divergence
from scipy.stats import jarque_bera, shapiro
from scipy.stats import fisher_exact
import numpy as np
import math


def squared_hist(s):
    content = bytearray(open(s, 'rb').read())
    freq =np.histogram(content,bins=256)
    total_dist=0
    for elem in freq[0]:
       total_dist+=math.pow(elem.astype(int)-(len(content)/256),2)
    return total_dist

#gtest and others
def correlations(s):
    data = np.fromfile(s, np.ubyte)
    b = np.bincount(data)
    # g1, p1 = power_divergence(b, lambda_="log-likelihood") #gtest
    # g2, p2 = power_divergence(b, lambda_="neyman") #gtest
    # g3, p3 = power_divergence(b, lambda_="freeman-tukey") #gtest
    # g4, p4 = power_divergence(b, lambda_="cressie-read") #gtest
    g5, p5 = jarque_bera(b) #gtest
    g6, p6 = shapiro(b) #gtest 
    #g5, p5 = power_divergence(b, lambda_="mod-log-likelihood") #gtest
    return [g5, g6]

def main():
    opts = argparse.ArgumentParser(prog='StatSeeker', description=__doc__)

    opts.add_argument('-a', action='store_true', help="run all test batteries")
    opts.add_argument('-v', '--version', action='version', version="0.1")
    opts.add_argument("--path", type=dir_path, help="one or more files to process")

    args = opts.parse_args()

    file_names = []
    #ent_results = []
    #fips2results = []
    #fips2stats = []
    #ais31results = []

    init_csv()

    for root, dir, files in os.walk(args.path):
        for file in files:
            path = os.path.join(root, file)
            fs = os.stat(path)

            size = 50000  # defeault 1024000
            num_runs = 10  # ideally >10, more is better

            print(path)

            if fs.st_size >= (size*num_runs)/8:
                file_names.append(path)

                file_info(path, fs.st_size)

                ent_results = ent(path)
                ent_csv(path, ent_results)
                #print(ent_results)
                print('ent')

                r, c, i = fips140(path, 2, 1000)
                fips2results = r
                fips2stats = c
                fips_csv(path, fips2results, fips2stats, i)
                print('fips2')

                # ais31 disabled until autocorrelation test can be fixed and optimisations made
                #ais31results = ais31(path)
                #if 'Nan' not in ais31results:
                #    ais_csv(path, ais31results)
                #print('ais31')

                if int(fs.st_size/(size/8)) < 10:
                    num_runs = int(fs.st_size/(size/8))

                print(num_runs)

                os.system('sudo bash ./sts_testscript.bash ' + str(path) + ' ' + str(size) + ' ' + str(num_runs) + ' > /dev/null')
                sp80022_csv(path, 'sts-2.1.2/experiments/AlgorithmTesting/finalAnalysisReport.txt')
                print('sp800-22')

                
                # p = Popen(["./darren_special_comp.bash", str(path)], stdout=PIPE, stderr=PIPE, stdin=PIPE)
                # output = str(p.stdout.read(),'utf-8')
                # output = output.split(", ")
                #print(output)
                # zips_csv(path,output)
                #print(output)

                #os.system('bash ./darren_special_del_comp.bash ' + str(path))

                ##other corrs
                corrs = correlations(path)
                corrs_csv(path,corrs)

                sq_hist = squared_hist(path)
                sq_csv(path,sq_hist)
                
                
                #add sp800-90B - figure out if it is possible to reduce them inimum file size

    #merge csvs
    csv_merge()

if __name__ == '__main__':
    main()
