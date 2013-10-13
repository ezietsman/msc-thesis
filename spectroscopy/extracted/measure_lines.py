# measure Ha,Hb and HeII line centres using gaussians

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

files = os.listdir(os.curdir)
ff = []
for f in files:
    name,ext = os.path.splitext(f)
    if name[:2] == 'EC':
        ff.append(f)



Lines = {}

Lines['Ha'] = [6500,6625,6563]
Lines['Hb'] = [4800,4925,4860]
Lines['HeII'] = [4620,4750,4686]




for line in ['Ha','Hb','HeII']:
    for f  in ff:
        print f
        
        # open spectrum and calculate continuum level near Ha line then write to cursor file
        data = pf.getdata(f)
        head = pf.getheader(f)
        start = head['CRVAL1']
        step = head['CDELT1']
        length = head['NAXIS1']
        x = start + pl.arange(0,length)*step
        hi = x > Lines[line][0]
        low = x < Lines[line][1]
        xx = hi*low
        med = pl.median(data[xx])
        print med
        cursor = open('cursor','w')
        cursor.write('%s %s 1 k\n%s %s 1 k\n'%(Lines[line][0],med,Lines[line][1],med))
        cursor.close()
        
        iraf.splot(images=f,\
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
        times.append(float(head['HJD']))

    # plot results
    
    results = pl.array(results)
    times = pl.array(times)
    fwhm = pl.array(fwhm)
    cen = Lines[line][2]
    kms = ((results-cen)/cen)*2.99792458e5
    
    #pl.subplot(211)
    #pl.plot(times-int(times[0]),fwhm,'.')
    #pl.xlabel('Time (HJD)')
    #pl.ylabel('FWHM (Angstrom)')
    
    
    #pl.subplot(212)
    #pl.plot(times-int(times[0]),kms,'.')
    #pl.xlabel('Time (HJD)')
    #pl.ylabel('Line Velocity (km/s)')
    #pl.ylim(-250,250)
    #pl.show()
    
    
    temp = pl.zeros((len(times),4),dtype='float')
    for i in range(len(times)):
        temp[i,0] = times[i]
        temp[i,1] = results[i]
        temp[i,2] = kms[i]
        temp[i,3] = fwhm[i]
    
    pl.save('%s.dat'%line,temp)
    
    results = []
    times= []
    kms = []
    fwhm = []



# plot the velocities of the lines and the photometry lightcurve







