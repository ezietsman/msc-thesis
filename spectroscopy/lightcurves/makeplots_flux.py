# Script to plot equivalent width time-series curves.
import pylab as pl
import astronomy as ast

Lines = {}
Lines['Red'] = 'red.dat'
Lines['Yellow'] = 'yellow.dat'
Lines['Blue'] = 'blue.dat'


pl.figure(figsize=(8,6))
pl.subplots_adjust(wspace=0.001,hspace=0.4)

# ephemeris
T0 = 2453964.3307097
P = 0.1545255

# make all the plots
for line,color,marker,n in zip(['Red','Yellow','Blue'],['r','g','b'],['.','x','+'],[1,2,3]):
    # plot the lightcurves
    pl.subplot(211)
    X = pl.load(Lines[line])
    x = X[:,0]
    p = (x-T0)/P
    ew = X[:,1]
    pl.plot(p,X[:,1]+0.2*n,'%s%s'%(color,marker),label=line)
    #p_ave = pl.movavg(p,40)
    #ew_ave = pl.movavg(ew,40)
    #pl.plot(p_ave,ew_ave+0.2*n,'%s-'%color)
    #pl.ylim(-55,5)
    #pl.legend(loc='lower left')
    pl.grid()

    # plot periodograms
    pl.subplot('23%s'%(n+3))
    if n ==1:
        pl.ylabel('Amplitude')
    if n == 2:
        pl.xlabel('Frequency (c/d)')


    # calculate periodograms
    f,a = ast.signal.dft(x,ew,0,4000,1)
    pl.plot(f,a,'k',label=line)
    #pl.xticks(pl.arange(0,4000,1000),[str(x) for x in (86400.0/pl.arange(0,4000,1000)).round(1)])
    pl.xticks(pl.arange(0,4000,1000))
    pl.xlim(0,4000)
    pl.ylim(0,0.02)
    pl.legend()


# modify tick labels
for n in [2,3]:
    pl.subplot('23%s'%(n+3))
    l = pl.gca().get_yticklabels()
    pl.gca().set_yticklabels(l,visible=False)


# add some axis labels
pl.subplot(211)
pl.ylabel('Intensity')
pl.xlabel('Orbital Phase')
pl.title('Intensity curves')

pl.savefig('fluxlc.png')
pl.show()