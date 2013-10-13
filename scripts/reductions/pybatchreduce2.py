#!/usr/bin/python

# script to call echomop programs one by one on each frame.
# written by Ewald Zietsman April 2007

import os
import string

# read list file. list contains the filenames of spectra to be extracted
filelist = open('list','r')
files = filelist.readlines()

# this removes the first one i.e. the manually reduced spectrum from the list. Comment this line if that
# file is not in the list.
del files[0] 

# now loop through the all files except first one
for spec in files:
    
    # get the filename and extension
    name, ext = os.path.splitext(string.strip(spec))
    
    
    #*********************************************************************************************
    # Create the reduction commands. Each is a list of strings that make up the complete commands
    # They are then joined to make a single string and run.
    #*********************************************************************************************
    
    # ECH_LOCATE    - echmenu 1
    #-------------
    ech_locate = ['/star/bin/echomop/ech_locate',\
    'ECH_RDCTN=dat%s'%name, \
    'tune_clone=ccd12']#,\
    #'INPTIM=%s' %name ]
        
    # ECH_TRACE     - echmenu 2
    #-------------
    ech_trace = ['/star/bin/echomop/ech_trace',\
    'ECH_RDCTN=dat%s'%name, \
    'tune_clone=ccd12']#,\
    #'INPTIM=%s' %name ]
    
    # ECH_FITORD    - echmenu 3
    #--------------
    ech_fitord = ['/star/bin/echomop/ech_fitord',\
    'ECH_RDCTN=dat%s'%name, \
    'tune_clone=ccd12']#,\
    #'INPTIM=%s' %name ]
    
    # ECH_SPATIAL   - echmenu 4
    #--------------
    ech_spatial = ['/star/bin/echomop/ech_spatial',\
    'ECH_RDCTN=dat%s'%name, \
    #'tune_clone=ccd12']#,\
    'SLITIM=P200608170397_12cc',\
    'PFL_INTERACT=no',\
    'PFL_MODE=A',\
    'TUNE_OBJABV=8',\
    'TUNE_OBJBLW=8',\
    'TUNE_MXSKYPIX=201',\
    'INPTIM=%s' %name ]
    
    # ECH_SKY   - echmenu 6
    #---------------
    ech_sky = ['/star/bin/echomop/ech_sky',\
    'ECH_RDCTN=dat%s'%name, \
    'FFIELD=P200608170397_12cc',\
    'PHOTON_TO_ADU=1.0',\
    'READOUT_NOISE=10.2',\
    'SKYFIT=median',\
    'TUNE_MXSKYPIX=201',\
    'TUNE_NOFLAT=yes',\
    'INPTIM=%s' %name ]
    
    # ECH_PROFILE   - echmenu 7
    #----------------
    ech_profile = ['/star/bin/echomop/ech_profile',\
    'ECH_RDCTN=dat%s'%name, \
    'tune_clone=ccd12',\
    'TUNE_MXSKYPIX=201']
    #'INPTIM=%s' %name ]
    
    
    # ECH_EXTRCT    - echmenu 8
    #----------------
    ech_extrct = ['/star/bin/echomop/ech_extrct',\
    'ECH_RDCTN=dat%s'%name, \
    #'tune_clone=ccd12',\
    'ARC=\"\'P200608170396_12cc,P200608170060_12cc\'\"',\
    'EXTRACT_MODE=\'O\'',\
    'FFIELD=P200608170397_12cc',\
    'PHOTON_TO_ADU=1.0',\
    'READOUT_NOISE=10.2',\
    'TUNE_MXSKYPIX=201',\
    'TUNE_CRCLEAN=yes',\
    'INPTIM=%s' %name ]
    
    # ECH_LINLOC    - echmenu 9
    #----------------
    ech_linloc = ['/star/bin/echomop/ech_linloc',\
    'ECH_RDCTN=dat%s'%name, \
    'tune_clone=ccd12']
    
    # ECH_IDWAVE    - echmenu 10
    #----------------
    ech_idwave = ['/star/bin/echomop/ech_idwave',\
    'ECH_RDCTN=dat%s'%name, \
    'tune_clone=ccd12',\
    'ECH_FTRDB=\'$ARCDIRS/CUAR\'']
    
    # ECH_RESULT    - echmenu 14
    #----------------
    ech_result = ['/star/bin/echomop/ech_result',\
    'ECH_RDCTN=dat%s'%name, \
    'RESULT_FORMAT=\'ASCII\'', \
    'RESULT_TYPE=\'EXTOBJ\'',\
    'ECH_RDUCD=ob_%s' %name ,\
    'ASCII_FILE=ob_%s.txt'%name]
    
    #************************************************************************************
    # Run the commands.
    #************************************************************************************
    os.system(string.join(ech_locate))
    os.system(string.join(ech_trace))
    os.system(string.join(ech_fitord))
    os.system(string.join(ech_spatial))
    os.system(string.join(ech_sky))
    os.system(string.join(ech_profile))
    os.system(string.join(ech_extrct))
    os.system(string.join(ech_linloc))
    os.system(string.join(ech_idwave))
    os.system(string.join(ech_result))
    
    # move all output files to 'objects' folder (only works in Linux :-))
    os.system('mv ob_* objects')
    
    
    
