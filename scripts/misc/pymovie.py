#make a movie of the spectra

import pylab as pl
import os

for i in range(61,396):
    print 'Plotting , ',i
    temp = pl.load('spec%04d.dat'%i)
    pl.plot(temp[:,0],temp[:,1])
    pl.ylim(-200,1500)
    pl.title('EC2117-54 Spectrum no. %s' %i)
    pl.xlabel('Wavelength')
    pl.ylabel('Counts')
    pl.savefig('tmp%04d.png'%i)
    #pl.show()
    pl.clf()
    
# encode the movie
#os.system("mencoder 'mf://*.png' -mf type=png:fps=25 -ovc lavc -lavcopts vcodec=wmv2 -oac copy -o animation.mpg")



