import numpy as np
import matplotlib.pyplot as plt
from essentials import *
import healpy as hp
NSIDE = 32
def give_skymap(batch):
    with open('./cmb-power-spectrum.txt') as csvfile:
        spectra = filereader(csvfile)
        l = spectra.T[0]
        tt = spectra.T[1]
        te = spectra.T[2]
        ee = spectra.T[3]
        bb = spectra.T[4]
        pp = spectra.T[5]
    
    batch_map=[]
    k = 0
    for _ in range(batch):
        skymap = hp.synfast(tt,NSIDE,new=True,verbose=False)
        skymap.resize(split(len(skymap)))
        batch_map.append(skymap) 

    return batch_map

def give_badskymap(batch,fnl=1e-4):
    with open('./cmb-power-spectrum.txt') as csvfile:
        spectra = filereader(csvfile)
        l = spectra.T[0]
        tt = spectra.T[1]
        te = spectra.T[2]
        ee = spectra.T[3]
        bb = spectra.T[4]
        pp = spectra.T[5]
    
    batch_map=[]
    k = 0
    for _ in range(batch):
        skymap = np.array(hp.synfast(tt,NSIDE,new=True,verbose=False))
        sqmap = np.square(skymap)
        skymap = skymap + (fnl/2.725)*(sqmap - np.full_like(skymap,np.mean(sqmap)))
        skymap.resize(split(len(skymap)))
        batch_map.append(skymap) 

    return batch_map

def get_res():
    return split(hp.nside2npix(NSIDE))

