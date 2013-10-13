# function to find x and y closest to xlick and yclick
#from numpy import *
from pylab import *


def smooth(x,y,n):
	xnew = [None]*0
	ynew = [None]*0
	end = len(x)
	k = 0
	xave = 0.0
	yave = 0.0
	
	for i in range(end):
		if k == n:
			xnew.append(xave/n)
			ynew.append(yave/n)
			xave = 0.0
			yave = 0.0
			k = 0
		
		elif i == end:
			xnew.append(xave/(k+1))
			ynew.append(yave/(k+1))
			
		else:
			xave += x[i]
			yave += y[i]
			k += 1
	
	
	return xnew,ynew

def find_nearest(x,y,xclick,yclick):
	
	temp = zeros(len(x),'d')
	
	#calculate distances to (xlick,yclick)
	temp[:] = ((x[:]-xclick)**2.0 + (y[:]-yclick)**2.0)**0.5
	minimum = temp.min()
		
	# This may be slow for large datasets -> Should find better way to do
	k = 0
	while True:
		if temp[k] == minimum:
			return k
			break
		else:
			k += 1
	


def plot_points(x1,y1,x2,y2):
	cla()
	plot(x1,y1,'x')
	plot(x2,y2,'ro')
	xlim(min(x1),max(x1))
	ylim(max(y1)+0.1,min(y1)-0.1)
	title('Left Click : Select          Right Click : Delete last point')
	xlabel('Close window when done to see spline')
	draw()
	return 0


