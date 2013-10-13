# pyraf script to do spectrum extractions

import os
import pylab as pl
import string
import pyfits as pf

# start IRAF
cd = os.getcwd()
try:
    print 'Trying /home/lemoen/'
    os.chdir('/home/lemoen/')
except:
    print 'We must be on corvus then... trying /home/ezietsman/'
    os.chdir('/home/ezietsman/')
    
from pyraf import iraf
os.chdir(cd)
try:
    os.remove('splot.log')
except:
    pass
# load NOAO package
iraf.noao()
iraf.astutil()
iraf.onedspec()


times = []
results = []
fwhm = []

for i in range(61,395):
    print i
    
    # open spectrum and calculate continuum level near Ha line then write to cursor file
    data = pf.getdata('fec2117_%04d.fits'%i)
    head = pf.getheader('fec2117_%04d.fits'%i)
    start = head['CRVAL1']
    step = head['CDELT1']
    length = head['NAXIS1']
    x = start + pl.arange(0,length)*step
    hi = x > 4640
    low = x < 4730
    xx = hi*low
    med = pl.median(data[xx])
    print med
    cursor = open('cursor','w')
    cursor.write('4640 %s 1 k\n4730 %s 1 k\n'%(med,med))
    cursor.close()
    
    iraf.splot(images='fec2117_%04d.fits'%i,\
    cursor='cursor',\
    save_file='splot.log')
    
    # read splot.log and extract the results
    myfile = open('splot.log','r')
    lines = myfile.readlines()
    try:
        # the first log written to empty file has header
        temp = string.split(string.strip(lines[3]))
        results.append(float(temp[0]))
        fwhm.append(float(temp[5]))
    except:
        temp = (string.split(string.strip(lines[2])))
        results.append(float(temp[0]))
        fwhm.append(float(temp[5]))
    # remove the log file
    myfile.close()
    os.remove('splot.log')
    
    # read the HJD from the fits header
    head = pf.getheader('fec2117_%04d.fits'%i)
    times.append(float(head['HJD']))




results = pl.array(results)
times = pl.array(times)
kms = ((results-4686.0)/4686.0)*2.99792458e5

pl.subplot(211)
pl.plot(times-int(times[0]),fwhm,'.')
pl.xlabel('Time (HJD)')
pl.ylabel('FWHM (Angstrom)')


pl.subplot(212)
pl.plot(times-int(times[0]),kms,'.')
pl.xlabel('Time (HJD)')
pl.ylabel('Line Velocity (km/s)')
pl.ylim(-400,400)
pl.show()


temp = pl.zeros((len(times),2),dtype='float')
for i in range(len(times)):
    temp[i,0] = times[i]
    temp[i,1] = kms[i]

pl.save('HeIIVel.dat',temp)


