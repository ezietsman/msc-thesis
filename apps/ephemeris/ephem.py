# program to read files containing lightcurves and calculate eclipse ephemeris

import numpy as N
import scipy.optimize as opt
import scipy.interpolate as sci
from astronomy import *
import os
import pylab as pl
import fitephem
# read the data file

os.system('ls -l')
myfile = raw_input('Enter file name : ')
x,y = utils.read_file(myfile)
x = N.array(x,'d')
y = N.array(y,'d')

print 'subtracting Julian date integer, %f ' %int(x[0])
x[:] = x[:] - int(x[0])

# plot lightcurve

pl.plot(x,y,'.')
pl.ylim(max(y)+0.25, min(y)-0.25)
pl.show()

# Some useful parameters

t = float(raw_input('Enter approx time of first eclipse : '))
period = float(raw_input('Enter approx period : '))
width = float(raw_input('Enter width around eclipse to use : '))
num  = float(raw_input('Enter no of points to use for spline : '))

ecl_times = []   # times of eclipse
cycle = []       # eclipse number



# fit spline to every num point in x,y
j = pl.arange(0,len(x),int(num))
cof = sci.splrep(x[j],y[j],k=3)
ynew = sci.splev(x,cof)

#function needed by fminbound
def func(p):
    return -1.0*sci.splev(p,cof)



# calculate the eclipse minimum for first eclipse

t0 = opt.fminbound(func,t - width/2.0, t + width/2.0)
ecl_times.append(t0)
cycle.append(0)
pl.vlines(t0,max(y)+0.25, min(y)-0.25,color='r',linestyle='solid')


def countx(a,b):
    # count number of elements in x between a and b
    count = 0
	
    try:
        for i in range(len(x)):
	   if x[i] > a:
	       if x[i] < b:
                   count += 1
               else:
                   return count
        return count
    except:
        return count 


# now calculate the eclipse minimum for every period thereafter

i = 1
t = t0 +  period*i

while t < x[-1]:

    count = countx(t-width/2.0, t+width/2.0)
    
    if count > 300:
        print i, count, t - width/2.0, t + width/2.0
        t = opt.fminbound(func,t - width/2.0, t + width/2.0)
        pl.vlines(t,max(y)+0.25, min(y)-0.25,color='k',linestyle='solid')
        pl.vlines(t - width/2.0,max(y)+0.25, min(y)-0.25,color='k',linestyle='dashed')
        pl.vlines(t + width/2.0,max(y)+0.25, min(y)-0.25,color='k',linestyle='dashed')
        #period = (t - t0) / i
        ecl_times.append(t)
        cycle.append(i)
        

    
    i += 1
    t = t0 +  period*i
    #period = (t - t0) / i
    
    
    
    
    
for i in range(len(ecl_times)):
    print cycle[i], ecl_times[i]

pl.plot(x,y,'.',x,ynew,'r-')
pl.ylim(max(y)+0.25, min(y)-0.25)
pl.show()

cof = pl.polyfit(cycle,ecl_times,1)

m,c,sm,sc = fitephem.fitephem(cycle,ecl_times)

ynew = m*N.array(cycle) + c

print 'Solutions'
print '---------'
print 'Period %s +- %s' % (m,sm)
print 'T0 %s +- %s'% (c,sc)
print
print 'Sum Square of res : ',sum((ecl_times - ynew)**2)



pl.subplot(211)
pl.plot(cycle,ecl_times,'k.')
pl.plot(cycle,ynew,'g-')
pl.xlim(min(cycle)-5,max(cycle)+5)
pl.xlabel('Cycle Number')
pl.ylabel('Eclipse time (days)')

pl.subplot(212)
pl.plot(cycle,(ecl_times-ynew)*86400.0,'k.')
pl.xlim(min(cycle)-5,max(cycle)+5)
pl.xlim(min(cycle)-5,max(cycle)+5)
pl.xlabel('Cycle Number')
pl.ylabel('Residuals (s)')
pl.show()




