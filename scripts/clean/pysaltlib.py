# module that contains useful functions
import string as S
import numpy as N
import pylab as pl


def returnbiassec(bias):
    # function takes the 'biassec' header entry and returns the bias strip limits xlo,xhi,ylo,yhi values as integers
    temp = S.split(S.strip(bias),',')
    xlo = int(S.split(temp[0],':')[0])
    xhi = int(S.split(temp[0],':')[1])
    ylo = int(S.split(temp[1],':')[0])
    yhi = int(S.split(temp[1],':')[1])
    
    return xlo,xhi,ylo,yhi
    

def subtract_bias(image,biaslimits):
    # takes data section as returned by pyfits and calculates the bias using median of the
    # biassec as in header entry
    
    xlo,xhi,ylo,yi = biaslimits
    image = N.array(image)
    print '\tBias limits: ',xlo,xhi,ylo,yi
    
    # calculate the median of the bias section
    # flatten changes the 2D array to single column array
    bias = N.median(image[:,xlo:xhi].flatten())
    
    print '\tBias: ', bias
    # subtract bias
    image[:,:] -= bias
    
    return image


def recon_ccd(image1,image2,ccdno):
    # takes images from 2 amps from ccd and reconstructs the original ccd image
    # also correct the dead column between the amps
    # ccdno must be 1 to correct the second dead line on ccd1 on the RSS
    
    # hopefully this is correct :-)
    # 512*201*2
    
    # !!!!! N.B. These assume 2x2 prebinning. Take care if binning is different !!!!!
    temp = N.zeros(205824)
    temp.shape = (201,1024)
    
    temp[:,0:512] = image1[:,25:537]
    temp[:,512:1024] = image2[:,25:537]
    
       
    # correct the dead column
    for i in range(201):
        temp[i,512] = (temp[i,511] + temp[i,513]) / 2.0
        
    # correct the funny column on RSS's ccd1 (col 465 or so)
    if ccdno == 1:
        for i in range(201):
            temp[i,463] = (temp[i,462] + temp[i,465]) / 2.0
            temp[i,464] = (temp[i,462] + temp[i,465]) / 2.0
    return temp
    
    
    
def recon_header(header0,header,entries):
    #function attempts to reconstruct header for output FITS file.
    new_head = header
    
    # get entries frim Primary HDU and construct new header.
    for entry in entries:
        # try to get ebtry from header0
        try:
            new_head.update(entry,header0[entry])
        # maybe its in the secondary headers...
        except:
            new_head.update(entry,header[entry])
        
    # this is a messy fudge but otherwise ds9 don't show the entire image
    new_head.update('DATASEC','[1:2024,1:201]')
    #print new_head
    
    return new_head
   
    
    
    
    
    
    
    
