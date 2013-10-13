# makes plot for thesis
import pylab as pl
import pyfits as pf


head = pf.getheader('outof_eclipse.fits')
start = head['CRVAL1']
step = head['CDELT1']
length = head['NAXIS1']
x = start + pl.arange(0,length)*step

out_eclipse = pf.getdata('outof_eclipse_fixed.fits')
mid_eclipse = pf.getdata('mid_eclipse_fixed.fits')



pl.figure(figsize=(12,4))
pl.subplots_adjust(hspace=0.001,bottom=0.13,left=0.08,right=0.94)

pl.plot(x,out_eclipse,'k-')
pl.plot(x,mid_eclipse,'k-')
pl.xlabel('Wavelength (Angstrom)')
pl.ylabel('Flux (normalised)')


# mark some emission lines
pl.text(4080,0.0028,r'$H_{\delta}$',fontsize=14)
pl.vlines(4102,0.0025,0.0027,'k','solid')
pl.text(4320,0.0028,r'$H_{\gamma}$',fontsize=14)
pl.vlines(4340,0.0025,0.0027,'k','solid')
pl.text(4840,0.0028,r'$H_{\beta}$',fontsize=14)
pl.vlines(4860,0.0025,0.0027,'k','solid')
pl.text(6540,0.0028,r'$H_{\alpha}$',fontsize=14)
pl.vlines(6563,0.0025,0.0027,'k','solid')
pl.text(4655,0.0028,r'$He_{II}$',fontsize=14)
pl.vlines(4686,0.0025,0.0027,'k','solid')
pl.text(5370,0.0028,r'$He_{I}$',fontsize=14)
pl.vlines(5410,0.0025,0.0027,'k','solid')

# mark terrestrial lines
pl.text(6833,0.001,r'$\oplus$',fontsize=14)
pl.vlines(6870,0.0007,0.0009,'k','solid')



pl.xlim(3200,7100)
pl.ylim(0,0.0033)
pl.text(3400,0.0018,'out of eclipse')
pl.text(3400,0.0007,'mid-eclipse')

pl.savefig('in_out_eclipse.png')

pl.show()
