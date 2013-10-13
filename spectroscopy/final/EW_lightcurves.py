# calculate lightcurve by summing every spectrum

import os
import pylab as pl
import pyfits as pf
import astronomy as ast

os.system('ls EC*.fits > speclist')

try:
    os.remove('splot.log')
except:
    pass

speclist = file('speclist','r')

HJD = []
flux = []

for spec in speclist:
    # read data and header
    data = pf.getdata(spec)
    head = pf.getheader(spec)
    start = head['CRVAL1']
    step = head['CDELT1']
    length = head['NAXIS1']
    x = start + pl.arange(0,length)*step
    HJD.append(float(head['HJD']))

    


