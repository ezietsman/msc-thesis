# run splot using pyraf script to catch output

import os
import pylab as pl
import pyfits as pf
import astronomy as ast

cd = os.getcwd()
os.chdir('/home/ewald/')
from pyraf import iraf
os.chdir(cd)


iraf.onedspec()

# create list of files containing the fits filenames
os.system('ls EC*.fits > speclist')

try:
    os.remove('splot.log')
except:
    pass

speclist = file('speclist','r')

HJD = []


for spec in speclist:
    # read data and header
    data = pf.getdata(spec)
    head = pf.getheader(spec)
    start = head['CRVAL1']
    step = head['CDELT1']
    length = head['NAXIS1']
    x = start + pl.arange(0,length)*step
    HJD.append(float(head['HJD']))

    # calculate continuum level near emission line
    
    # Helium II
    #gt = x > 4600.0
    #lt = x < 4800.0
    
    # Hydrogen alpha
    #gt = x > 6400.0
    #lt = x < 6600.0
    
    # Hydrogen Beta
    gt = x > 4700.0
    lt = x < 4900.0
    
    continuum = pl.median(data[gt*lt])
    
    # write to cursor file
    cfile = open('cursor','w')
    #s = "4676 %s 1 e\n4696 %s 1 e\n" % (continuum,continuum)
    s = "4850 %s 1 e\n4870 %s 1 e\n" % (continuum,continuum)
    #s = "6553 %s 1 e\n 6573 %s 1 e\n" % (continuum,continuum)
    cfile.write(s)
    iraf.splot(images=spec.strip(),cursor='cursor')
     
# run bplot
#iraf.bplot(images='@speclist',cursor='cursor')

HJDfile = open('HJD.dat','w')
for d in HJD:
    HJDfile.write('%s\n'%d)
HJDfile.close()
    
    
# get the output. Tune this grep command for the wavelength
#os.system('grep 65 splot.log > rv.dat')


