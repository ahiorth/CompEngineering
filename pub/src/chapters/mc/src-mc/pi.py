import numpy as np
import random

def estimate_pi(N,d):
#   random.seed(2)
    D2=d*d/4; dc=0.5*d
    A=0
    for k in range(0,N):
        x=random.uniform(0,d)
        y=random.uniform(0,d)
        if((x-dc)**2+(y-dc)**2 <= D2):
            A+=1
    # estimate area of circle: d*d*A/N
    return 4*A/N

N=1000;d=2
pi_est=estimate_pi(N,d)
print('Estimate for pi= ', pi_est,' Error=', np.pi-pi_est)

NN=[100,1000,10000,100000]
for n in NN:
    pi_est=estimate_pi(n,d)
    print(pi_est,pi_est-np.pi,n,1/np.sqrt(n), sep=',')
