#!/usr/bin/python
# script to automate some of the tasks that needed to be done manually in IRAF(bleh!) for SALT spectra
# designed to work on raw SALT data i.e. Files containing 1 header unit and 6 image units

# IMPORTANT: script assumes 2x2 pre-binning since my data was like this. 

# Run in directory containing raw SALT spectra. New FITS files are written with suffix _12cc, _34cc and _56cc for ccd 1 to 3

# New images are bias subtracted using median of bias section, gain corrected using custom gain values for the separate amplifiers and are mosaiced to give the original ccd images. The dead column between amps are interpolated.

# written by Ewald Zietsman 04/05/2007 


import pyfits
import os
import numpy as N
import numarray as num  # still need numarray since pyfits use that. Change when pyfits uses numpy.
import string as S

import pysaltlib as pslib

# PARAMETERS- change these for specific dataset
#------------------------------------------------------------------------#

# gains
# !!!! Change these for specific dataset !!!!
# default values determined from eg21 spectrophotometric standard using imstat on edges of ccd-> pwoudt
gain = [10.5,11.3,10.7,10.0,9.5,9.25]





# change these as desired. Make sure they are in either the Primary or first extension headers
header_entries = ['RA','DEC','OBJECT','UTC-OBS','OBSERVAT','DATE-OBS','GAIN','RDNOISE','EXPTIME',
                  'CTYPE1','CTYPE2','EQUINOX','CRPIX1','CRPIX2','CRVAL1','CRVAL2','CDELT1',
                  'CDELT2','BITPIX','NAXIS','NAXIS1','NAXIS2','PCOUNT','GCOUNT','CCDSUM']

#------------------------------------------------------------------------#
# Hopefully no changes below this will be needed

# first find all files in the directory
fitslist = os.listdir('.')

# now open every fits image,split it into its various parts and update the headers
for fits in fitslist:
    # use try: except: blocks to get rid of those other pesky files
    try:
        # empty list to keep images in
        images = []
        headers = []
       
        rootname = fits[:-5]
        
        # now open the fits file.
        HDU = pyfits.open(fits)
        print '\nProcessing: ',fits
        # read every image and apply gain corrections, mosaic back into separate ccd images
        for i in range(1,len(HDU)):
            header = HDU[i].header

            # get the bias strip and bias correct the images
            print '\tCalculating bias: '
            biassec = pslib.returnbiassec(header['biassec'][1:-1])
            data = HDU[i].data
            data = pslib.subtract_bias(data,biassec)                        
            
            # multiply images with gain corrections specified at beginning of file
            print '\tApplying gain correction: ', gain[i-1]
            data *= gain[i-1]

            # save bias corrected images in list
            images.append(data)
            headers.append(header)  

            print ''
            #name = root + '_' + str(i) + '.fits'
            #pyfits.writeto(name,data,header=header)

       # read headers and write to big header file
       # do this properly later
        print "\tReconstructing header : %s " % fits
        header0 = HDU[0].header
        header  = headers[0]
        new_head = pslib.recon_header(header0,header,header_entries)
               
        # now mosaic arrays to make the full ccd images again and write to disk
        # also muliply 'fudge factor' to make the spectrum continuous across ccd's
        # !!!!!!!!!  NB convert images to numarray arrays. Change when pyfits moves to numpy!!!!!!!!!!!!
        
        print '\tReconstructing CCD images: CCD1'
        frame12 = num.array(pslib.recon_ccd(images[0],images[1],1))
        filename = rootname + '_12cc.fits'
        pyfits.writeto(filename,frame12,header=new_head)
        
        print '\tReconstructing CCD images: CCD2'
        # multiply by 0.98
        frame34 = 1.1*num.array(pslib.recon_ccd(images[2],images[3],2))
        filename = rootname + '_34cc.fits'
        pyfits.writeto(filename,frame34,header=new_head)
        
        print '\tReconstructing CCD images: CCD3'
        # Multiply by 1.15
        frame56 = 1.15*num.array(pslib.recon_ccd(images[4],images[5],3))
        filename = rootname + '_56cc.fits'
        pyfits.writeto(filename,frame56,header=new_head)
            
    # tried to open non-FITS file
    except:
        # skip this one
        print 'Error: %s not raw SALT spectrum. Skipping to next file' % fits
        continue
