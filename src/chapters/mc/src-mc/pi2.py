import numpy as np

def f(x,D2):
    return 2*np.sqrt((D2-x*x))

def mcm_mean(N,d):
    D2=d*d/4
    x=np.random.uniform(-d/2,d/2,size=N)
    A=np.sum(f(x,D2))
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
