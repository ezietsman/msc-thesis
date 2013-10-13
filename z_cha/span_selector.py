#!/usr/bin/env python
"""
The SpanSelector is a mouse widget to select a xmin/xmax range and plot the
detail view of the selected region in the lower axes
"""
import numpy as npy
from pylab import figure, show
import pylab as pl
from matplotlib.widgets import SpanSelector
import os
import string
import scipy.interpolate as sci
import astronomy as ast

# create figure
fig = figure(figsize=(8,9))
ax = fig.add_subplot(311)


# read in data
os.system('ls -l')
filename = raw_input('Open which file ? : ')
os.system('less %s' % filename)
cols = string.split(raw_input('Use which columns ? : '))

# load a lightcurve
X = pl.load(filename)
x = X[:,int(cols[0])-1]
#y = 10**(X[:,int(cols[1])-1]/(-2.5))
y = X[:,int(cols[1])-1]

yyy = None
 

    
# make variables to store selected ranges
ranges = []
polys = []

ax.plot(x, y, '-')
#ax.set_ylim(-2,2)
ax.set_title('Raw lightcurve: select range to flatten using polynomial')

ax2 = fig.add_subplot(312)
line2, = ax2.plot(x,y,'.')

ax3 = fig.add_subplot(313)
line3, = ax3.plot(x,y,'.')

def fit_data(xval,yval,n):
    # fit poly of order n to x,y and return poly values
    ave_x = npy.average(xval)
    ave_y = npy.average(yval)
    
    cof = pl.polyfit(xval-ave_x,yval-ave_y,n)
    ynew = pl.polyval(cof,xval-ave_x)
    return xval,ynew+ave_y



def onselect(xmin, xmax):
    global yyy
    # this runs after the selection has been made
    tb = pl.get_current_fig_manager().toolbar
    if tb.mode == '':
            
        # find indices of selection
        indmin, indmax = npy.searchsorted(x, (xmin, xmax))
        indmax = min(len(x)-1, indmax)
        
        # add selected range to list
        ranges.append([indmin,indmax])
        
        
        thisx = x[indmin:indmax]
        thisy = y[indmin:indmax]
        
        # fit polynomial to selected data
        n = input('Order of polynomial to fit ? : ')
        xx,yy = fit_data(thisx,thisy,n)
        polys.append(yy)
        
        # plot polynomial on middle plot over raw data
        ax2.plot(xx,yy,'r-')
        
        yyy = y.copy()
        
        # subtract selected ranges from lightcurve
        for r in range(len(ranges)):
            yyy[ranges[r][0]:ranges[r][1]] -= polys[r]
            line3.set_data(x,yyy)
            #ax3.plot(x,yyy,'.')

        
        fig.canvas.draw()

# set useblit True on gtkagg for enhanced performance
span = SpanSelector(ax, onselect, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.1, facecolor='red') )


# after eclipses have been removed, the rest of the lightcurve must be normalised too. maybe use spline
# on points not in the ranges variable

show()


original = pl.zeros(len(x))

for i in range(len(ranges)):
    original[ranges[i][0]:ranges[i][1]] += 1

no_eclipse = original < 1

# fit spline to points outside eclipse
#l = pl.arange(0,len(x[no_eclipse]),20)
tck = sci.splrep(x[no_eclipse],y[no_eclipse],k=3,s=0.75)
ynew = sci.splev(x[no_eclipse],tck)

# subtract spline
yyy[no_eclipse] -= ynew



# plot results.
pl.figure()
pl.subplot(211)
pl.plot(x,yyy,'.')
pl.plot(x[no_eclipse],ynew,'r-')


pl.subplot(212)
f,a = ast.signal.dft(x,yyy,0,4000,1)
pl.plot(f,a,'k')

show()


temp = []
temp.append(x)
temp.append(yyy)
temp.append(y - yyy)


pl.save('flat.dat',pl.array(temp).transpose())

