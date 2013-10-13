import pylab as pl
import astronomy as ast

LC = pl.load('S6061r_FF.dat')
x = LC[:,0]
y = LC[:,1]
f,a = ast.signal.dft(x,y,0,4000,1)

OC = pl.load('oc_out.dat')

pl.figure(figsize=(8,6))
pl.subplots_adjust(hspace=0.001,wspace=0.35,right=0.98)


ax1 = pl.subplot(321)
pl.scatter(x-int(x[0]),y,0.01,'k',label='Lighcurve')

yl=pl.ylim()
for et in [0.4225,0.4971]:
    pl.vlines(et,-0.06,0.06,color='k')
yt = pl.yticks()[0]
pl.yticks(yt[2:])
pl.ylim(-0.06,0.06)
pl.ylabel('Intensity')
pl.xlim(0.35,0.55)

ax2 = pl.subplot(323,sharex=ax1)
t = OC[:,2]
amp = OC[:,0]
siga = OC[:,3]
pl.errorbar(t-int(t[0]),amp,siga,fmt='ro')
pl.ylabel('Amplitude')
for et in [0.4225,0.4971]:
    pl.vlines(et,-0.005,0.02,color='k')
yt = pl.yticks()[0]
pl.yticks(yt[2:-1])
pl.ylim(-0.005,0.02)
pl.xlim(0.35,0.55)



ax3 = pl.subplot(325,sharex=ax1)
p = OC[:,1]
sigp = OC[:,4]
pl.errorbar(t-int(t[0]),p,sigp,fmt='go')
pl.ylabel('Phase (O-C)')
pl.xlabel('Heliocentric Julian Date (+2451581)')
yl=pl.ylim()
for et in [0.4225,0.4971]:
    pl.vlines(et,-2,2,color='k')
yt = pl.yticks()[0]
pl.yticks(yt[1:-1])
pl.ylim(-2,2)
pl.xlim(0.34,0.55)


ax4 = pl.subplot(122)
pl.plot(f,a,'k-',label='Periodogram')
pl.xlabel('Frequency (c/d)')
pl.ylabel('Amplitude')
xt = pl.xticks()[0]
pl.xticks(xt[1:-1:2])
yt = pl.yticks()[0]
pl.yticks(yt[1:])
pl.ylim(0,0.003)
pl.vlines(3420,0.0024,0.0026)
pl.text(3250,0.00265,'DNO')

xtl = pl.setp(ax1.get_xticklabels()+ax2.get_xticklabels() , visible=False)

pl.savefig('z_cha_OC_FT.png')

pl.show()