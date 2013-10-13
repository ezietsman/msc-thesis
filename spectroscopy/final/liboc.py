from numpy import *
from numpy.linalg import *


def oc(y,t,freq,N):
	# Calculates o-c (amplitude and phase) diagram given lightcurve (x,y) , frequency and 
	# N integer cycles to use per point
	# overlaps N/2 of every cycle
	# t is in time units
	
	# assume no gaps in data for now
	dt = t[1] - t[0]
	period = 1.0 / freq
	
	fitlength = int(N * period / dt)
	
	#print fitlength
	print len(t)
	
	amp = []
	sigamp = []
	phi = []
	sigphi = []
	date = []
	
	for i in range(0,len(t),int(fitlength/2.0)):
		
		if i + fitlength/2.0 <= len(t):
			x = fitwave(y[i:i+fitlength],t[i:i + fitlength],freq)
			
			amp.append(x[0])
			phi.append(x[1])
			sigamp.append(x[2])
			sigphi.append(x[3])
			date.append(sum(t[i:i + fitlength]) / len(t[i:i+fitlength]))
		else:
			x = fitwave(y[i:len(t)+1],t[i:len(t)+1],freq)
			amp.append(x[0])
			phi.append(x[1])
			sigamp.append(x[2])
			sigphi.append(x[3])
			date.append(sum(t[i:-1]) / len(t[i:-1]))
		
		
	print i

	amp = array(amp)
        # try to fix wrapping problem
	phi = array(phi) / ( pi)
        
        for i in range(len(phi)-1):
            if phi[i+1] - phi[i] > 0.5:
                phi[i+1] -= 1.0
                
            elif phi[i+1] - phi[i] < -0.5:
                phi[i+1] += 1.0
                
        for i in range(len(phi)-1):
            integer = int(phi[i+1] - phi[i])
            phi[i+1] -= integer

        #phi += 0.5
        #greater = phi > 0.5
        #phi[greater] -= 1.0
        #greater = phi < -0.48
        #phi[greater] += 1.0
	sigamp = array(sigamp)
	sigphi = array(sigphi) / (pi)
	date = array(date)
	
	return amp,phi,date,sigamp,sigphi
	
	

def fitwave(y,t,freq):
	# function that fits a sine wave (given frequency) to data points y-t 
	# and returns A and phi and their uncertainties
	#print len(t)
	# initial values
	amp = 0.001
	phi = 0.5
	converged = False
	amp_old = amp
	phi_old = phi
	
	while not converged:
		A = zeros(len(t)*2.0,'d')
		l = transpose(y.copy())
		
		sine = sin(2.0*pi*freq*t + phi)
		cosine = amp*cos(2.0*pi*freq*t + phi)*2.0*pi
		
		#Build A and l matrix
		A.shape = (len(t),2)
		A[:,0] = sine[:]
		A[:,1] = cosine[:]
		
		# Calculate x-vector
		At = transpose(A)
		AtA = dot(At,A)
		E  = inv(AtA)
		Atl = dot(At,l)
		x = dot(E,Atl)
		
		amp = x[0]
		phi += x[1]
		
		# make sure 0.0 =< phi =< 2*pi
		if phi > pi:
			phi -= 2*pi
		elif phi < -1*pi:
			phi += 2*pi
		
		
		#make sure the amplitude are positive
		if amp < 0.0:
			amp *= -1.0
			#if phi > pi:
				#phi -= pi
			#else:
				#phi += pi
		
		
		if abs(amp - amp_old) < 0.00001 and abs(phi - phi_old) < 0.00001:
			converged = True
		else:
			amp_old = amp
			phi_old = phi 
		
	# calculate uncertainties
	
	v = dot(A,x) - l
	vv2 = dot(transpose(v),v)
	sigma2 = vv2 / (len(t) - 2)
	E *= sigma2
	
	return amp,phi, sqrt(E[0][0]) , sqrt(E[1][1])