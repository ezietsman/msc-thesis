#!/usr/bin/python
#showspec

import pylab as pl
import pyfits as p
import string

myfile = open('list','r')
mylist = myfile.readlines()

# make synthetic 'wavelength' ranges

x1 = pl.arange(0,1024)
x2 = pl.arange(1074,2098)
x3 = pl.arange(2148,3172)

image = pl.zeros((335,3172))

for i in range(0,len(mylist)-3,3):
    #print '%s of %s' % (i,len(mylist))
    im1 = p.getdata(string.strip(mylist[i]))
    im2 = p.getdata(string.strip(mylist[i+1]))
    im3 = p.getdata(string.strip(mylist[i+2]))
    image[i/3,0:1024] = im1[0,:]
    image[i/3,1074:2098] = im2[0,:]
    image[i/3,2148:3172] = im3[0,:]
    #pl.figure(figsize=(12,12))    
    #pl.plot(x1,im1[0,:],x2,im2[0,:],x3,im3[0,:])
    #pl.show()

pl.figure(figsize=(16,4))
pl.plot(image.sum(axis=1))
pl.title('Lightcurve')

pl.figure(figsize=(16,4))
pl.gray()
pl.imshow(image,vmin=100,vmax=600,interpolation='nearest')
pl.title('Trailed Spectrogram')

pl.show()