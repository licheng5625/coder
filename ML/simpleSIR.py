import scipy.integrate as spi
import numpy as np
import pylab as pl

beta=1.4247
gamma=0.14286
I0=0.01
ND=48
TS=1.0
INPUT = (1.0-I0, I0)

def diff_eqs(p,t,INP):
	'''The main set of equations'''
	Y=np.zeros((2))
	V = INP

	Y[0] = - beta * V[0] * V[1] + gamma * V[1]
	Y[1] = beta * V[0] * V[1] - gamma * V[1]
	return Y   # For odeint



t_start = 0.0; t_end = ND; t_inc = TS
t_range = np.arange(t_start, t_end+t_inc, t_inc)
RES = spi.odeint(diff_eqs,INPUT,t_range)

print (RES)

#Ploting
pl.subplot(211)
pl.plot(RES[:,0], '-g', label='Susceptibles')
pl.title('Program_2_5.py')
pl.xlabel('Time')
pl.ylabel('Susceptibles')
pl.subplot(212)
pl.plot(RES[:,1], '-r', label='Infectious')
pl.xlabel('Time')
pl.ylabel('Infectious')
pl.show()