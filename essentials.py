import math
import csv
#import tqdm
import numpy as np

def makefloatarray(row):
    k = row[0].split()
    l = []
    for blah in k:
        try:
            l.append(float(blah))
        except ValueError:
            #print(k)
            break
    return l

def filereader(csvfile):
    spice_cl = []
    readCSV = csv.reader(csvfile,delimiter='\n')  
    for row in readCSV:
        l = makefloatarray(row)
        if l != []:
            spice_cl.append(l)
            
    return np.array(spice_cl)

def split(x):
  k = math.floor(math.sqrt(x))
  while float(x)/k != math.floor(float(x)/k):
      k = k+1
  return (int(k),int(x/k),1)

