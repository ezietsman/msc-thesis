# make movie of the spectra :-)

import pyfits as pf
import pylab as pl
import os
#import astronomy as ast
import scipy.interpolate as sci





# Read the spectra from the disk

files = os.listdir(os.curdir)
ff = []
for f in files:
    name,ext = os.path.splitext(f)
    if name[:2] == 'EC':
        ff.append(f)

# Get the wavelength to pixel info from the first fits header
head = pf.getheader(ff[0])
start = float(head['CRVAL1'])
step = float(head['CDELT1'])
length = float(head['NAXIS1'])
x = start + pl.arange(length)*step



c = 2.99792458e5
#l0 = 6563 # Ha
#l0 = 4860 # HeII
#l0 = 4686 # Hb

#lines = {}
#lines['Ha'] = 6563
#lines['Hb'] = 4686
#lines['HeII'] = 4860

# construct continuum light curve by masking off the emission line areas and integrating


v = 3500.0

# HeII
#dl = v/c*4680
#a1 = x < 4680 - dl
#a2 = x > 4680 + dl

dl1 = 700.0/c*4686
dl2 = 800.0/c*4686
a1 = x < 4680 - dl1
a2 = x > 4680 + dl2

# Hb
dl = v/c*4860
b1 = x < 4860 - dl
b2 = x > 4860 + dl
# Ha
dl = v/c*6563
c1 = x < 6563 - dl
c2 = x > 6563 + dl

# masks for continuum and emission regions
cont = (a1+a2)*(b1+b2)*(c1+c2)
#em = cont == False

ha = c1+c2 == False
hb = b1+b2 == False
heii = a1+a2 == False

time = []
continuum = []
Ha = []
Hb = []
HeII = []


for f in ff:
    print 'Creating lightcurves from file %s\n\n' % f
    data = pf.getdata(f)
    time.append(pf.getheader(f)['HJD'])
    
    print 'Creating:   Continuum lightcurve'

    continuum.append(data[cont].sum())
    
    print 'Fitting spline to continuum'
    # now fit a cubic spline to continuum regions and subtract
    #tck = sci.splrep(x[cont],data[cont],k=1)
    #y = sci.splev(x,tck)
    
    ## try fitting third order poly to continuum
    #p = pl.polyfit(x[cont],data[cont],3)
    #y = pl.polyval(p,x)
    #data -= y
    
    #pl.plot(x,data+y,'.')
    #pl.plot(x,y,'r-')
    #pl.plot(x,data,'k-')
    #pl.show()
    
    # now integrate (very simple, no weights for now) each emission line separately
    print 'Creating:   Emission line lightcurves\n\n\n'
    Ha.append(data[ha].sum())
    Hb.append(data[hb].sum())
    HeII.append(data[heii].sum())
    
time = pl.array(time)

#pl.plot(x[em],pf.getdata(ff[0])[em])
#pl.show()


#for line in ['Ha','Hb','HeII']:
    #print line
    #l0 = lines[line]
    ## Add pixels within v km/s from the line centre
    #v = 2000.0
    #hi = x > l0*(1 - v/c)
    #low = x < l0*(1 + v/c)
    #xx = hi*low

    #lc = [pf.getdata(f)[xx].sum() for f in ff]
    #time = [float(pf.getheader(f)['HJD']) for f in ff]
    
    #lc = -2.5*pl.log10(pl.array(lc))
    #time = pl.array(time)

lines = {}
lines['Ha'] = Ha
lines['Hb'] = Hb
lines['HeII'] = HeII
lines['Cont'] = continuum
time = time[:-2]
# save the lightcurves to file
for line in ['Ha','Hb','HeII','Cont']:
#for line in ['HeII']:
    lc = pl.array(lines[line])[:-2]
    #lcmean = lc.mean()
    #lc = lc - lcmean
    ##temp = pl.zeros((len(lc),3),dtype='float')
    
    ## flatten lightcurves by fitting 11th order poly to them
    #tmean = time.mean()

    #p = pl.polyfit(time-tmean,lc,13)
    #yy = pl.polyval(p,time-tmean)
    #print yy
    temp = []
    temp.append(time)
    temp.append(lc)
    #temp.append(lc-yy)
    
    #for i in range(len(lc)):
        #temp[i,0] = time[i]
        #temp[i,1] = lc[i]
        #temp

    pl.save('speclc_%s.dat'%line,pl.array(temp).transpose(),fmt='%1.6f')

