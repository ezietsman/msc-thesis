# make transform HJD to orbital phase for OC diagrams

import pylab as pl
import os
import string




# archive ephemeris


def makeplot(X,hjd,filename,ephem):

    
    if ephem == 1:
        # archive ephem
        T0 = 2452525.374416
    elif ephem == 2:
        # august ephem
        T0 = 2453964.330709

    P = 0.154525
    
    #X = pl.load(filename)
    a = X[:,0][:-1]
    p = X[:,1][:-1]
    x = (X[:,2][:-1]+hjd-T0)/P - int(((X[:,2][:-1]+hjd-T0)/P)[0])
    siga = X[:,3][:-1]
    sigp = X[:,4][:-1]
    
    temp = []
    temp.append(a)
    temp.append(p)
    temp.append(x)
    temp.append(siga)    
    temp.append(sigp)
    
    pl.save(filename[:-4] + 'OP' + '.dat',pl.array(temp).transpose())
        
    

if __name__ == '__main__':
    os.system('ls -l')
    filename = raw_input('Open which file ? : ')
    hjd = int(raw_input('Add how much to fix Julian Date? : '))
    ephem = int(raw_input('Use Archive ephem (1) or August (2) : '))
    X = pl.load(filename)
    makeplot(X,hjd,filename,ephem)
    