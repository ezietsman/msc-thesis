# compare my spectra to patrick's

import pylab as pl
import pyfits as pf
import os

# first
files = os.listdir(os.curdir)
ff = []
for f in files:
    name,ext = os.path.splitext(f)
    if name[:2] == 'EC':
        ff.append(f)



l = ['A','B','C','D','E','F','G','H','I','J']


for i in range(len(l)):
    
    P12 = pl.load('EC2117_12%s.txt'%l[i])
    P56 = pl.load('ec2117_56%s.txt'%l[i])
    
    P = pl.concatenate([P12,P56])
    data = pf.getdata(ff[i])
    head = pf.getheader(ff[i])
    start = head['CRVAL1']
    step = head['CDELT1']
    length = head['NAXIS1']
    x = start + pl.arange(0,length)*step
    

    
    pl.subplot(211)
    pl.plot(x,data)
    pl.plot(P[:,0],P[:,1],'r')
    #pl.plot(P56[:,0],P56[:,1]*3e7,'r')
    #pl.xlim(4660,4720)
    pl.xlabel('Wavelength (Angstrom)')
    pl.ylabel('Flux ')
    pl.legend(('Ewald','Patrick'))
    pl.grid()
    
    pl.subplot(212)
    pl.plot(x,data)
    pl.plot(P[:,0],P[:,1],'r')
    #pl.plot(P56[:,0],P56[:,1]*3e7,'r')
    pl.xlim(6500,6600)
    pl.xlabel('Wavelength (Angstrom)')
    pl.ylabel('Flux ')
    pl.legend(('Ewald','Patrick'))
    pl.grid()
    pl.show()
