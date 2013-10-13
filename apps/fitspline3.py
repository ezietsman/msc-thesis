#! /usr/bin/python

# program to fit various splines to lightcurve

from pylab import *
from astronomy import *
from os import system
from libfitspline import *
from scipy.interpolate import splrep,splev

corrected = []
xspline = [None]*0
yspline = [None]*0
k_old	= 0

# select points with mouse
def on_click(event):
	global k_old
    # get the x and y coords, flip y from top to bottom
	x, y = event.x, event.y
	if event.button==1:
		if event.inaxes is not None:
			# find the point in the lightcurve that is nearest to the clicked coordinates
			k = find_nearest(date,mag,event.xdata,event.ydata)
			
			N = int(raw_input('How many points to smooth? : '))
			
			temp = smooth(date[k_old:k],mag[k_old:k],N)
			
			xspline.append(date[k_old+1])
			yspline.append(mag[k_old+1])
					
			for i in range(len(temp[0])):
				xspline.append(temp[0][i])
				yspline.append(temp[1][i])
			
			xspline.append(date[k])
			yspline.append(mag[k])
			
			temp = []	
			k_old = k 
			     
	#elif event.button==3:
		## delete last added point
		#if event.inaxes is not None:
			#k = len(xspline) - 1
			#del xspline[k]
			#del yspline[k]
			#plot_points(date,mag,xspline,yspline)
			
connect('button_press_event', on_click)

# get the points from the file
system('ls -l')
date,mag = read_file_interactive(raw_input("Enter filename "))
date = array(date)
mag = array(mag)


# plot the light curve
plot(date,mag,'x')
length = max(date) - min(date)

xlim(min(date)-length / 10.0 ,max(date)+ length / 10.0)
ylim(max(mag)+0.1 , min(mag)-0.1)
title('Left Click : Select end section to be used.')
xlabel('Close window when done to see splines')
show()

xspline = array(xspline)
yspline = array(yspline)

#xspline[:] = xspline[:] - int(xspline[0])


plot(date,mag,'x')
plot(xspline,yspline,'r-')
xlim(min(date),max(date))
ylim(max(mag)+0.1 , min(mag)-0.1)
show()

for i in range(len(xspline)):
	print xspline[i], yspline[i]

tck = splrep(xspline,yspline)
ynew = splev(date,tck)

# plot lightcurve and splinepoints and spline
subplot(211)

plot(date,mag,'x')
plot(date,ynew,'r-')
plot(xspline,yspline,'ro')
xlim(min(date),max(date))
ylim(max(mag)+0.1 , min(mag)-0.1)
xlabel('HJD')
ylabel('Magnitude')
title('Lightcurve with fitted spline')

subplot(212)
#plot lightcurve - spline
plot(date,mag-ynew,'gx')
xlim(min(date),max(date))
ylim(max(mag-ynew)+0.1 , min(mag-ynew)-0.1)
title('Lightcurve minus fitted spline')
xlabel('HJD')
ylabel('Magnitude - Spline')
show()





# write to file
outfile = raw_input("Enter output filename  [output.dat] : ")

if len(outfile) == 0:
	myfile = file("output.dat",'w')
else:
	myfile = file(outfile,'w')

for i in range(len(date)):
	s = str(date[i]) + "	" + str(round(mag[i]-ynew[i],4)) + "	" + str(round(ynew[i],4)) + "\n"
	myfile.write(s)
	


