#! /usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from essentials import *
import healpy as hp
NSIDE = 32
def give_skymap(batch,fnl=1e-3):
    with open('./cmb-power-spectrum.txt') as csvfile:
        spectra = filereader(csvfile)
        l = spectra.T[0]
        tt = spectra.T[1]
        te = spectra.T[2]
        ee = spectra.T[3]
        bb = spectra.T[4]
        pp = spectra.T[5]
    
    skymap = hp.synfast(tt,NSIDE,new=True,verbose=False)
    sqmap = np.square(skymap)
    skymap = skymap + (fnl/2.725)*(sqmap - np.full_like(skymap,np.mean(skymap)**2))
    ttprime = np.array(hp.anafast(skymap)) 
    batch_map=[]
    k = 0
    for _ in range(batch):
        skymap = hp.synfast(ttprime,NSIDE,new=True,verbose=False)
        #skymap = skymap/np.mean(skymap)
        #skymap = skymap/np.std(skymap)
        #skymap.resize(split(len(skymap)))
        #batch_map.append(skymap) 
        alms = hp.map2alm(skymap))
        alms.resize(split(len(alms)))
        batch_map.append(alms) 

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
        skymap = skymap + (fnl/2.725)*(sqmap - np.full_like(skymap,np.mean(skymap)**2))
        #skymap = skymap/np.mean(skymap)
        #skymap = skymap/np.std(skymap)
        #ttprime = np.array(hp.anafast(skymap,lmax=2506)) 
        #scale = np.dot(tt , ttprime)/(np.dot(tt , tt))
        #skymap.resize(split(len(skymap)))
        #batch_map.append(skymap)
        alms = hp.map2alm(skymap))
        alms.resize(split(len(alms)))
        batch_map.append(alms) 

    return batch_map

def get_res():
    return split(hp.nside2npix(NSIDE))
if __name__ == "__main__":
    give_badskymap(2)
    give_badskymap(2,1e5)
