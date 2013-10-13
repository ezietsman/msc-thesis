# make plots of the signal to noise

import pylab as pl

X = pl.load('snr_curves.dat')

# ephemeris
T0 = 2453964.3307097
P = 0.1545255


phase = (X[:,0]-T0)/P

pl.figure(figsize=(6,4))
for col,reg,c in zip([1,4,5],[r'$H_{\alpha}$',r'$H_{\beta}$','$He_{II}$'],['r-','g-','b-']):
    pl.plot(phase,X[:,col],c,label=reg)
pl.title('SNR of emission lines')
pl.xlabel('Orbital Phase')
pl.ylabel('Signal-to-noise')
pl.ylim(0,35)
pl.legend(loc='best')
pl.savefig('line_snr.png')


pl.figure(figsize=(6,3))
pl.subplots_adjust(right=0.9,left=0.1,bottom=0.15)
for col,reg,c in zip([2,3,6],['Red','Yellow','Blue'],['r-','g-','b-']):
    pl.plot(phase,X[:,col],c,label=reg)
pl.title('SNR of continuum regions')
pl.xlabel('Orbital Phase')
pl.ylabel('Signal-to-noise')
pl.legend(loc='best')
pl.savefig('continuum_snr.png')

pl.show()