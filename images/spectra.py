# make plots of the uncalibrated and calibrated spectra of EG21 and EC2117

import pyfits as pf
import pylab as pl



# EG21 spectra

raw = pf.getdata('EG21_new.fits')

pl.figure(figsize=(6,4))
pl.subplots_adjust(left=0.14)
pl.plot(raw,'k')
pl.title('Uncalibrated EG21 Spectrum')
pl.xlabel('Pixel numbers')
pl.ylabel('Counts')
pl.savefig('uncalEG21.png')

cal = pf.getdata('EG21_flux.fits')
head = pf.getheader('EG21_flux.fits')
x = pl.arange(len(cal),dtype='d')
x = x * float(head['CDELT1']) + float(head['CRVAL1'])

pl.figure(figsize=(6,4))
pl.subplots_adjust(left=0.14)
pl.plot(x,cal,'k')
pl.title('Calibrated EG21 Spectrum')
pl.xlabel('Wavelength (Angstrom)')
pl.ylabel('Flux (erg/cm^2/s/A)')
pl.savefig('calEG21.png')



# averaged EC2117 spectrum

ec = pf.getdata('EC2117.fits')
head = pf.getheader('EC2117.fits')
x = pl.arange(len(ec),dtype='d')
x = x * float(head['CDELT1']) + float(head['CRVAL1'])

pl.figure(figsize=(6,4))
pl.subplots_adjust(left=0.14)
pl.plot(x,ec,'k')
print min(x),max(x)
#pl.title('Calibrated EC21178-5417 Spectrum')
pl.xlabel('Wavelength (Angstrom)')
pl.ylabel('Flux (erg/cm^2/s/A)')

# add some line ids

pl.text(4080,3e-14,r'$H_{\delta}$',fontsize=14)
pl.vlines(4102,0.0,2.8e-14,'k','dashed')
pl.text(4320,3e-14,r'$H_{\gamma}$',fontsize=14)
pl.vlines(4340,0.0,2.8e-14,'k','dashed')
pl.text(4840,3e-14,r'$H_{\beta}$',fontsize=14)
pl.vlines(4860,0.0,2.8e-14,'k','dashed')
pl.text(6540,3e-14,r'$H_{\alpha}$',fontsize=14)
pl.vlines(6563,0.0,2.8e-14,'k','dashed')
pl.text(4655,3.5e-14,r'$HeII$',fontsize=14)
pl.vlines(4686,0.0,3.3e-14,'k','dashed')
pl.text(5370,3e-14,r'$HeI$',fontsize=14)
pl.vlines(5410,0.0,2.8e-14,'k','dashed')


pl.ylim(0.0,4e-14)
pl.xlim(min(x),max(x))


pl.savefig('EC2117.png')




# high-speed EC2117 exposure



ec = pf.getdata('EC0010.fits')
head = pf.getheader('EC0010.fits')
x = pl.arange(len(ec),dtype='d')
x = x * float(head['CDELT1']) + float(head['CRVAL1'])

pl.figure(figsize=(6,4))
pl.subplots_adjust(left=0.14)
pl.plot(x,ec,'k')
#pl.title('Calibrated EC21178-5417 Exposure')
pl.xlabel('Wavelength (Angstrom)')
pl.ylabel('Flux (erg/cm^2/s/A)')

# add some line ids

pl.text(4840,5e-14,r'$H_{\beta}$',fontsize=14)
pl.vlines(4860,0.0,4.8e-14,'k','dashed')
pl.text(6540,5e-14,r'$H_{\alpha}$',fontsize=14)
pl.vlines(6563,0.0,4.8e-14,'k','dashed')
pl.text(4655,5.5e-14,r'$HeII$',fontsize=14)
pl.vlines(4686,0.0,5.2e-14,'k','dashed')


pl.ylim(0.0,6e-14)
pl.xlim(min(x),max(x))


pl.savefig('EC0010.png')












pl.show()