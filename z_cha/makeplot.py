# program to make plots of the lightcurves for inclusion in dissertation
import pylab as pl
import astronomy as ast
from matplotlib.ticker import FormatStrFormatter
fmt = FormatStrFormatter('%1.2g')  # or whatever


X = pl.load('S6061r_FF.dat')
x1 = X[:,0]
y1 = X[:,1] 
z1 = X[:,2]

pl.figure(figsize=(6,4))
pl.subplots_adjust(hspace=0.6,left=0.16)
ax = pl.subplot(211)
pl.scatter(x1-int(x1[0]),y1,marker='o',s=0.1,color='k')
pl.ylim(-1.0e-6,1.0e-6)
pl.xlim(min(x1-int(x1[0])),max(x1-int(x1[0])))
pl.ylabel('Intensity')
pl.xlabel('HJD +%s'%int(x1[0]))


ax.yaxis.set_major_formatter(fmt)


pl.subplot(212)
f,a = ast.signal.dft(x1,y1,0,4000,1)
pl.plot(f,a,'k')
pl.ylabel('Intensity')
pl.xlabel('Frequency (c/d)')
yl = pl.ylim()

pl.savefig('S6061.png')


pl.show()