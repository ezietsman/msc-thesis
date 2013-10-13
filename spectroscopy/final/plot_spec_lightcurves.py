# plot the spectrum lightcurves

import pylab as pl


pl.figure(figsize=(9,6))

pl.subplots_adjust(hspace=0.001)


T0 = 2453964.3307097
P = 0.1545255

X = pl.load('speclc_HeII.dat')

x = (X[:-2,0] - T0)/P

#ax1 = pl.subplot(411)
pl.plot(x,X[:-2,1],'b.',label=r'$HeII$')
#yl = pl.ylim()

#yt = pl.yticks()
#pl.yticks(yt[0][1:-1])
#pl.ylim(yl[1],yl[0])
#pl.legend(loc='lower left')




X = pl.load('speclc_Ha.dat')
#ax2 = pl.subplot(412)
pl.plot(x,X[:-2,1],'r.',label=r'$H_{\alpha}$')
#yl = pl.ylim()

#yt = pl.yticks()
#pl.yticks(yt[0][2:-1])
#pl.ylim(yl[1],yl[0])
#pl.legend(loc='lower left')
    
X = pl.load('speclc_Hb.dat')
#ax3 = pl.subplot(413)
pl.plot(x,X[:-2,1],'g.',label=r'$H_{\beta}$')
#yl = pl.ylim()
#yt = pl.yticks()
#pl.yticks(yt[0][1:-2])
#pl.ylim(yl[1],yl[0])
#pl.legend(loc='lower left')

X = pl.load('speclc_Cont.dat')
#ax4 = pl.subplot(414)
pl.plot(x,X[:-2,1],'.',color='orange',label='Continuum')
#yl = pl.ylim()
#yt = pl.yticks()
#pl.yticks(yt[0][2:-1])

    
#pl.ylim(18,11)

#xl = pl.xlim()
# plot photometry lightcurve
#X = pl.load('run2_flat.dat')
#pl.plot(X[:,0]-1,X[:,1]+X[:,2],'k.',label='photometry')
    
#xticklabels = ax1.get_xticklabels() + ax2.get_xticklabels()+ax3.get_xticklabels()
#pl.setp(xticklabels, visible=False)
#yl = pl.ylim()
#pl.ylim(yl[1],yl[0])
pl.ylabel('Relative Magnitude')
pl.xlabel('Orbital Phase')
pl.legend(loc='lower left')
#pl.xlim(xl[0],0.59)
pl.show()
