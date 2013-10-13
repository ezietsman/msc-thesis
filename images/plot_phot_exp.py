import pylab as pl
import pyfits as pf

im = pf.getdata('a0022000.fts')
pl.imshow(im,cmap=pl.cm.gray_r,vmin=0,vmax=2500,interpolation='nearest')
pl.quiver([12.5],[30],[0],[10])
pl.yticks([])
pl.xticks([])
pl.savefig('ec2117_phot_exp.png')
pl.show()

