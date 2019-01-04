import numpy as np
import csv
import tqdm
import matplotlib.pyplot as plt
def makefloatarray(row):
    k = row[0].split()
    l = []
    for blah in k:
        try:
            l.append(float(blah))
        except ValueError:
            print(k)
            break
    return l

def filereader(csvfile):
    spice_cl = []
    readCSV = csv.reader(csvfile,delimiter='\n')  
    for row in tqdm.tqdm(readCSV):
        l = makefloatarray(row)
        if l != []:
            spice_cl.append(l)
            
    return np.array(spice_cl)
with open('./cmb-power-spectrum.txt') as csvfile:
    spectra = filereader(csvfile)
    l = spectra.T[0]
    tt = spectra.T[1]
    te = spectra.T[2]
    ee = spectra.T[3]
    bb = spectra.T[4]
    pp = spectra.T[5]

import healpy as hp
skymap = hp.synfast(tt,32,new=True)
print(skymap)
print(len(skymap))


