import csv
import os
import pandas as pd

HEADER_ent = ['File name', 'Entropy', 'Chi-score']
#HEADER_zips = ['File name', 'zip_ratio', 'bzip_ratio', 'rar_ratio', 'gzip_ratio', 'magics', 'revmagics']
HEADER_corrs = ['File name','jarque-bera','shapiro']
HEADER_sq = ['File name','squared_hist']
HEADER_fips = ['File name', 'Iterations', 'Monobit', 'Poker', 'Run', 'Long run', 'Continuous']
#HEADER_ais31 = ['File name', 'T0', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6a', 'T6b', 'T7a_1', 'T7a_2', 'T7b_1', 'T7b_2', 'T7b_3', 'T7b_4', 'T8']
HEADER_sp80022 = ['File name', 'Frequency', 'Block Frequency', 'Cumulative Sums', 'Overlapping Template']
HEADER_fileinfo = ['File name', 'size']


def init_csv():
    with open('results/fileinfo.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(HEADER_fileinfo)

    with open('results/ent_results.csv', "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(HEADER_ent)

    # with open('results/ais31_stats.csv', 'w') as f:
    #     writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     writer.writerow(HEADER_ais31)

    with open('results/fips_results.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(HEADER_fips)

    with open('results/fips_stats.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(HEADER_fips)

    with open('results/sp80022_stats.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(HEADER_sp80022)
    
    # with open('results/zips_stats.csv', 'w') as csvfile:
    #     writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     writer.writerow(HEADER_zips)
    with open('results/corrs_stats.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(HEADER_corrs)

    with open('results/sq_stats.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(HEADER_sq)

def dir_path(string):
    return string if os.path.isdir(string) else raiser(NotADirectoryError(string))


def file_info(path, size):
    with open('results/fileinfo.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([path, size])


# take results of ent and returns csv of results
def ent_csv(path, results):
    with open('results/ent_results.csv', "a") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        entropy, chi_score = results
        writer.writerow([path, entropy, chi_score])
        csvfile.close()

# def zips_csv(path, results):
#     with open('results/zips_stats.csv', "a") as csvfile:
#         writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#         zips=results[0]
#         bzip=results[1]
#         rar=results[2]
#         gzip=results[3]
#         magics=results[4]
#         revmagics=results[5]
#         writer.writerow([path, zips, bzip, rar, gzip, magics, revmagics])
#         csvfile.close()

def corrs_csv(path, results):
    with open('results/corrs_stats.csv', "a") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        g5=results[0]
        g6=results[1]
        writer.writerow([path, g5, g6])
        csvfile.close()

def sq_csv(path, results):
    with open('results/sq_stats.csv', "a") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        sq=results
        writer.writerow([path, sq])
        csvfile.close()


# take results of ais-31 (non-fips) tests and returns csv of results
# def ais_csv(path, r):
#     with open('results/ais31_stats.csv', 'a') as f:
#         writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         writer.writerow([path, r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]])


def aggregate_lists(data, index, num):
    aggregated = []
    for i in range(num):
        aggregated.append([])
        for j in range(len(data[index])):
            aggregated[i].append(data[index][j][i])
    return aggregated


def fips_csv(path, results, stats, it):
    with open('results/fips_results.csv', 'a') as csvfile:
        monobits = []
        pokers = []
        runs = []
        longruns = []
        continuous = []
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(results)):
            monobits.append(results[i][0])
            pokers.append(results[i][1])
            runs.append(results[i][2])
            longruns.append(results[i][3])
            continuous.append(results[i][4])

        writer.writerow([path, it, monobits.count(True), pokers.count(True), runs.count(True), longruns.count(True), continuous.count(True)])
        csvfile.close()

    with open('results/fips_stats.csv', "a") as csvfile:
        monobits = []
        pokers = []
        runs = []
        longruns = []
        #cont = []
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(stats)):
            monobits.append(stats[i][0])
            pokers.append(stats[i][1])
            runs.append(stats[i][2])
            longruns.append(stats[i][3])
            #cont.append(results[i][4])

        writer.writerow([path, it, monobits, pokers, runs, longruns])
        csvfile.close()

def sp80022_csv(path, res):
    temp = []
    with open(res, 'r') as results:
        readfile = results.readlines()[7:]
        for line in readfile:
            temp.append(line.split()[10:])
            #print(temp)
        with open('results/sp80022_stats.csv', 'a') as out:
            writer = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # p-values in x[0], proportion passed in x[1]
            # * indicates a failure
            writer.writerow([path, [[x[0] for x in temp if 'Frequency' in x],
                             [x[1] for x in temp if 'Frequency' in x]],
                             [[x[0] for x in temp if 'BlockFrequency' in x],
                             [x[1] for x in temp if 'BlockFrequency' in x]],
                             [[x[0] for x in temp if 'CumulativeSums' in x],
                             [x[1] for x in temp if 'CumulativeSums' in x]],
                             [[x[0] for x in temp if 'OverlappingTemplate' in x],
                             [x[1] for x in temp if 'OverlappingTemplate' in x]],])

# merges all csvs passed in as a list of csv names (default filenames only atm)
# returns single csv with individual files joined on file names with concatenated result columns


def csv_merge():
    x = pd.read_csv('results/fileinfo.csv')
    a = pd.read_csv('results/ent_results.csv')
    b = pd.read_csv('results/fips_stats.csv')
    c = pd.read_csv('results/sp80022_stats.csv')
    #d = pd.read_csv('results/zips_stats.csv')
    e = pd.read_csv('results/corrs_stats.csv')
    f = pd.read_csv('results/sq_stats.csv')

    a = a.dropna(axis=1)
    b = b.dropna(axis=1)
    c = c.dropna(axis=1)
    #d = d.dropna(axis=1)
    e = e.dropna(axis=1)
    f = f.dropna(axis=1)

    merged = x.merge(a, on='File name')
    merged = merged.merge(b, on='File name')
    merged = merged.merge(c, on='File name')
    #merged = merged.merge(d, on='File name')
    merged = merged.merge(e, on='File name')
    merged = merged.merge(f, on='File name')

    merged.to_csv("results/statistics.csv", index=False)

