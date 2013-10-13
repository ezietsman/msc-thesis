# Script to flatten lightcurve using a digital IIR filter

import scipy.signal as signal
import scipy.interpolate as interpolate
import pylab as pl
import astronomy as ast
import os
import string


os.system('ls -l')
filename = raw_input('Open which file ? : ')
os.system('less %s' % filename)
cols = string.split(raw_input('Use which columns ? : '))


# load a lightcurve
X = pl.load(filename)
x = X[:,int(cols[0])-1]
y = 10**(X[:,int(cols[1])-1]/(-2.5))


y = y/pl.average(y)


# we must interpolate this lightcurve to the minimum time spacing throughout
xnew,ynew = ast.signal.resample(x,y)

# subtract the first magnitude from lightcurve to avoid funny edge effects
ynew -= ynew[0]
dt = xnew[1]-xnew[0]
# now create filter coefficients
# filter parameters
fp = 144.0
fs = 100.0
wp = fp*pl.pi*dt*2.0/pl.pi
ws = fs*pl.pi*dt*2.0/pl.pi
gpass = 0.1
gstop = 15
ftype = 'cheby1'

#print wp
#print ws

# calculate filter coefficients and filter the lightcurve
b,a = signal.iirdesign(wp,ws,gpass,gstop,ftype=ftype)
yf = signal.lfilter(b,a,ynew)


yesno = raw_input('Plot results [y] ?')
if yesno == 'y' or yesno =='Y' or yesno == '':
    # plot some stuff
    pl.figure(figsize=(9,12))
    pl.subplot(411)
    pl.plot(xnew,yf,'.')
    #yl = pl.ylim()
    #pl.ylim(yl[1],yl[0])
    
    pl.subplot(412)
    pl.plot(xnew,ynew,'.')
    #yl = pl.ylim()
    #pl.ylim(yl[1],yl[0])
    
    pl.subplot(413)
    freq,amp = ast.signal.dft(xnew,yf,0,8000,1)
    pl.plot(freq,amp)
    
    pl.subplot(414)
    w,h = signal.freqs(b,a)
    pl.plot(w,h)
    pl.show()



# save lightcurve
temp = []
temp.append(xnew)
temp.append(yf)
temp.append(ynew-yf)



outfilename = string.strip(raw_input('Enter output filename [%s_FF.dat] : ' % filename[:-4]))
if outfilename == '':
    filename2 = '%s_FF.dat' % filename[:-4]
else:
    filename2 = outfilename
    
print 'Saving to %s' % filename
pl.save(filename2,pl.array(temp).transpose())


temp = []
temp.append(x)
temp.append(y)

pl.save('Norm%s'%filename,pl.array(temp).transpose())

