# make transform HJD to orbital phase for lightcurves

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
    x = (X[:,0]+hjd-T0)/P - int(((X[:,0]+hjd-T0)/P)[0])
    y = X[:,1]
    z = X[:,2]    
    
    temp = []
    temp.append(x)
    temp.append(y)
    temp.append(z)
    
    
    pl.save(filename[:-4] + 'OP' + '.dat',pl.array(temp).transpose())
        
    

if __name__ == '__main__':
    os.system('ls -l')
    filename = raw_input('Open which file ? : ')
    hjd = int(raw_input('Add how much to fix Julian Date? : '))
    ephem = int(raw_input('Use Archive ephem (1) or August (2) : '))
    X = pl.load(filename)
    makeplot(X,hjd,filename,ephem)
    