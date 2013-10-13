# Script to display lightcurve in blocks of 2000s

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
#y = 10**(X[:,int(cols[1])-1]/(-2.5))
y = X[:,int(cols[1])-1]

dt = 86400.0/2000.0



