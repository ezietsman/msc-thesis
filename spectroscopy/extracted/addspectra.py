# pyraf script to do add spectra together

import os
import string
import pyfits as pf
import numpy

## start IRAF
#cd = os.getcwd()
#try:
    #print 'Trying /home/lemoen/'
    #os.chdir('/home/lemoen/')
#except:
    #print 'We must be on corvus then... trying /home/ezietsman/'
    #os.chdir('/home/ezietsman/')
    
#from pyraf import iraf
#os.chdir(cd)

## load NOAO package
#iraf.noao()
#iraf.astutil()
#iraf.onedspec()


N = input('\nAdd how many spectra? : ')

print '\nfinding spectra...\n'
files = os.listdir(os.curdir)
files.sort()
ff = []
for f in files:
    name,ext = os.path.splitext(f)
    if name[:3] == 'fec':
        ff.append(f)
print '\nDone.\n'

k = 0
specno = 0
new = []
hjd = []

os.system('rm -v EC*')

for i in range(len(ff)+1):
    #print '%s of %s' % (i,len(ff))
    if i < len(ff):
        if k != N:
            new.append(pf.getdata(ff[i]))
            hjd.append(float(pf.getheader(ff[i])['HJD']))
            k += 1
        elif k == N:
            #myfile = open('comblist','w')
            #for n in new:
                #myfile.write(n+'\n')
                #print n
            
            # run scombine on files in comblist
            #iraf.scombine(input='@comblist',output='EC%04d.fits'%specno,combine='median')
            avehjd = numpy.average(hjd)
            print avehjd
            avenew = numpy.average(new,axis=0)
            newhead = pf.getheader(ff[0])
            newhead['HJD'] = avehjd
            pf.writeto('EC%04d.fits'%specno,avenew,newhead)
            
            specno += 1
            new = []
            hjd = []
            new.append(pf.getdata(ff[i]))
            hjd.append(float(pf.getheader(ff[i])['HJD']))
            #new.append(ff[i])
            k = 1
    elif i == len(ff):
        #myfile = open('comblist','w')
        #for n in new:
            #print n
           #myfile.write(n+'\n')
        #iraf.scombine(input='@comblist',output='EC%04d.fits'%specno,combine='median')
        avehjd = numpy.average(hjd)
        print avehjd
        avenew = numpy.average(new,axis=0)
        #avenew = numpy.average(new)
        newhead = pf.getheader(ff[0])
        newhead['HJD'] = avehjd
        pf.writeto('EC%04d.fits'%specno,avenew,newhead)
        
        specno+=1

print specno

#if len(new) != 0:
    ##myfile = open('comblist','w')
    ##for n in new:
        ##myfile.write(n+'\n')
        ##print n
    ##iraf.scombine(input='@comblist',output='EC%04d.fits'%specno,combine='median')
    #avehjd = pl.average(hjd)
    #print avehjd
    #avenew = pl.average(new)
    #newhead = pf.getheader(ff[0])
    #newhead['HJD'] = str(avehjd)
    #pf.writeto('EC%04d.fits'%specno,avenew,newhead)


