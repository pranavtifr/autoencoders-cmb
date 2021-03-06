#! /usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from essentials import *
import healpy as hp
NSIDE = 256 # You can change the NSIDE here to get better maps
'''
give_puremap() generates a map for the cl's read from the file cmb-power-spectrum.txt

give_skymap() generates a gaussian map for the cl's generated for a non gaussian map 
This is done to make sure that the power spectra is the same

give_badskymap() generates a non gaussian map for the given cl's
'''
def give_puremap(batch):
    with open('./cmb-power-spectrum.txt') as csvfile:
        spectra = filereader(csvfile)
        l = spectra.T[0]
        tt = spectra.T[1]
        te = spectra.T[2]
        ee = spectra.T[3]
        bb = spectra.T[4]
        pp = spectra.T[5]
    
    batch_map=[]
    for _ in range(batch):
            # The following function creates the map as an numpy array with nested ordering
        skymap = hp.synfast(tt,NSIDE,new=True,verbose=False) #You can also pass the other
                                                             # cls here to get better maps
        batch_map.append(skymap)
    return np.array(batch_map)



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
        batch_map.append(skymap) 
        #alms = hp.map2alm(skymap)
        #image = make_alm_image(alms)
        #alms.resize(split(len(alms)))
        #batch_map.append(image)

    return batch_map

def give_badskymap(batch,fnl=1e-3):
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
        batch_map.append(skymap)
        #alms = hp.map2alm(skymap)
        #alms.resize(split(len(alms)))
        #image = make_alm_image(alms)
        #batch_map.append(image)

    return batch_map

def get_res():
    return split(hp.nside2npix(NSIDE))

def make_alm_image(alms):
    print(alms)
    print(np.shape(alms))
    
    ssss = hp.sphtfunc.Alm()
    lmax = 3*NSIDE -1
    mag = np.zeros((lmax,lmax))
    phase = np.zeros((lmax,lmax))
    for l in range(lmax): 
        for m in range(l):
            mag[l][m] = np.abs(alms)[ssss.getidx(lmax,l,m)]
            phase[l][m] = np.angle(alms)[ssss.getidx(lmax,l,m)]
    return [mag,phase]



if __name__ == "__main__":
    k = give_puremap(1)  
    print(k[0])
    give_badskymap(1)
    #give_badskymap(2,1e5)
