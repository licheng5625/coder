import scipy.optimize as optimization

import scipy.integrate as spi
import numpy as np
import pylab as pl
import simpleSEIZ_fit
import simpleSIR_fit
import LMtext
mydat=[21, 46, 67, 83, 91, 99, 111, 120, 127, 129, 135, 141, 148, 174, 202, 223, 260, 287, 304, 319, 347, 369, 383, 411, 436, 460, 476, 512, 540, 555, 571, 588, 597, 610, 615, 618, 628, 636, 658, 684, 725, 751, 783, 808, 847, 891, 917, 938]
#kkk
mydat=[1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 17, 30, 34, 37, 46, 56, 86, 125, 172, 207, 248, 277, 299, 344, 394, 429, 463, 492, 518, 543, 560, 577, 590, 598, 608, 613, 618, 626, 631, 635, 638, 655, 674, 698, 712, 723, 734, 744]
#449
mydat=[1, 2, 4, 5, 7, 9, 9, 9, 11, 14, 18, 20, 20, 20, 22, 31, 37, 40, 49, 69, 72, 93, 108, 120, 121, 129, 131, 132, 136, 137, 140, 140, 141, 144, 144, 147, 147, 147, 147, 147, 151, 151, 151, 151, 151, 151, 151, 153, 153]
#1347
# mydat=[27, 80, 100, 117, 141, 150, 246, 355 ,397, 446, 462, 472, 481, 487, 498, 500, 502, 504, 505, 506, 510, 513, 517, 523, 525, 527, 531, 531, 533, 534, 535, 538, 538, 540, 541, 542, 542, 542, 542, 542, 543, 544, 544, 544, 546, 546, 546, 547, 548]
#Schumacher
mydat=mydat[:10]
def RSErr( x, y):
    t=min(len(x),len(y))
    if (t==0):
       return 0;
    val = 0.0;
    for i in range(0, t):
       val += (x[i] - y[i])**2;
    val=((val/ t)**0.5);
    return val;
if 1==0:
    mydat=np.array(mydat)

    p=simpleSIR_fit.fitSIS(mydat)
    RES=simpleSIR_fit.getdata(p,len(mydat))
    pl.plot(RES[:,1], '-r', label='SIS')
    #
    pl.plot( mydat/mydat[-1], '-b', label='real Infectious')
    print("SIS ERROR"+str(RSErr(RES[:,1],mydat/mydat[-1])))

    # p=simpleSEIZ_fit.fitSEIZ(mydat)
    # RES=simpleSEIZ_fit.getdata(p,len(mydat))
    # print(RES[:,2])
    # pl.plot(RES[:,2], '-g', label='SEIZ')
    # #
    # print("SEIZ ERROR"+str(RSErr(RES[:,2],mydat/mydat[-1])))
    # pl.legend(loc='upper left')
    #
    # pl.xlabel('Time(Hour)')
    # pl.ylabel('Infectious')
    # pl.show()
else:
    ds=[mydat[0]]
    for i in range(1,len(mydat)):
        ds.append(mydat[i]-mydat[i-1])
    LMtext.drawSpikeM(ds)