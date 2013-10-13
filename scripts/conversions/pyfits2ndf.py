# python script that uses the Starlink convert, fits2ndf program to convert all fits
# images in directory to ndf format

import os

mylist = os.listdir('.')
    
for fits in mylist:
    print fits
    name,ext = os.path.splitext(fits)
    if ext == '.fits':
        try:
            command = '/star/bin/convert/./fits2ndf %s %s' % (fits,name)
            os.system(command)
        except:
            continue
