# clean the cosmic rays from the spectrum

import pylab as pl
import os

cleaned = 0

for i in range(61,396):
    print 'Cleaning , ',i
    temp = pl.load('spec%04d.dat'%i)
       
    # run throught the spectrum and 
    # replace high and low values with the average of the adjacent values.
    med = pl.median(temp[:,1])
    greater = temp[:,1] > 3*med
    smaller = temp[:,1] < -200
    temp[greater,1] = med
    temp[smaller,1] = med
       
    outfile = pl.save('spec%04dc.dat'%i,temp)
