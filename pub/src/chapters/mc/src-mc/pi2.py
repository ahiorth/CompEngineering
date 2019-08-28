import numpy as np
import random

def f(x,D2):
    return 2*(D2-x*x)**0.5

def mcm_mean(N,d):
#   random.seed(2)
    D2=d*d/4
    A=0
    for k in range(0,N):
        x=random.uniform(-d/2,d/2)
        A+=f(x,D2)
    # estimate for area: A/N
    return d*A/N

N=1000;d=2
pi_est=mcm_mean(N,d)
print('Estimate for pi= ', pi_est,' Error=', np.pi-pi_est)

import pi
NN=[100,1000,10000,100000,1000000]
for n in NN:
    pi_est2=mcm_mean(n,d)
    pi_est=pi.estimate_pi(2*n,d)
    print("%.4f,%.4f,%.4f,%.4f, %d" % (pi_est2, pi_est2-np.pi,pi_est,pi_est-np.pi,n))
