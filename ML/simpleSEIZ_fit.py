import scipy.optimize as optimization

import scipy.integrate as spi
import numpy as np
import pylab as pl
# dat=[21,25,21,16,8,8,12,9,7,2,6,6,7,26,28,21,37,27,17,15,28,22,14,28,25,24,16,36,28,15,16,17,9,13,5,3,10,8,22,26,41,26,32,25,39,44,26,21,29]
dat=[21, 46, 67, 83, 91, 99, 111, 120, 127, 129, 135, 141, 148, 174, 202, 223, 260, 287, 304, 319, 347, 369, 383, 411, 436, 460, 476, 512, 540, 555, 571, 588, 597, 610, 615, 618, 628, 636, 658, 684, 725, 751, 783, 808, 847, 891, 917, 938, 967]

def diff_eqs(INP,t,para):
    '''The main set of equations'''
    beta=para[0]
    b=para[1]
    l=para[2]
    e=para[3]
    p=para[4]
    rho=para[5]
    Y=np.zeros((4))
    S=INP[0]
    E=INP[1]
    I=INP[2]
    Z=INP[2]
    N=S+I+E+Z
    Y[0] = - beta * S * I/N -b * S * Z/N
    Y[1] = (1-p)*beta * S * I/N +(1-l)*b * S * Z/N-rho*E*I/N-e*E
    Y[2] = - p*beta * S * I/N +rho * E * I/N+e*E
    Y[3] = l*b* S * Z/N
    return Y 

def getdata(p,timeEND):
    t_start = 1.0; t_end = timeEND; t_inc = 1.0
    t_range = np.arange(t_start, t_end+t_inc, t_inc)
    INPUT=p[6:]
    para=p[:6]
    RES = spi.odeint(diff_eqs,INPUT,t_range,args=(para,))
    #print(RES)
    return RES


def residuals(p, x, y,timeEND):
    #print RSErr(T,re,y)
    RES=getdata(p,49)
    return RES[:timeEND,2] - y


def fitSEIZ(dat):
    lentgh=len(dat)
    dat=np.array(dat)

    if lentgh==0:
        for i in range(10-lentgh):
            dat=np.append(dat,1)
    else:
        if lentgh<10:
            lastdata=dat[-1]
            for i in range(10-lentgh):
                dat=np.append(dat,lastdata)
        dat=dat/dat[-1]
    N=dat[-1]
    N0=dat[0]
    timeEND=len(dat)
    x0 =  [0.1,0.1,0.1,0.1,0.1,0.1,N,N0,0,0]
    p = optimization.leastsq(residuals,x0,maxfev=20000,ftol=1.49012e-10, xtol=1.49012e-10, args=( dat,dat,timeEND))[0]
    return p

# dat=np.array(dat)
#
# p=fitSEIZ(dat)
# # #p=[1-0.001,0.001,1.4247,0.14286]
# print(p)
# RES=getdata(p,48)
# print(RES[:,1])
# #Ploting
# pl.subplot(211)
# pl.plot(RES[:,0], '-g', label='Susceptibles')
# pl.title('Program_2_5.py')
# pl.xlabel('Time')
# pl.ylabel('Susceptibles')
# pl.subplot(212)
# pl.plot(RES[:,2], '-r', label='Infectious')
# pl.plot( dat/dat[-1], '-b', label='real Infectious')
#
# pl.xlabel('Time')
# pl.ylabel('Infectious')
# pl.show()
