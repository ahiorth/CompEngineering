from scipy.special import gamma
import random
import numpy as np

def f(x,R=1):
    r=R*R
    for xi in x:
      r-=xi*xi
    if(r<0):
        return 0.
    else:
        return 2*np.sqrt(r)

def int_trapez(lower_limit, upper_limit,func,x,i,N):
    h       = (upper_limit-lower_limit)/N
    x[i]=lower_limit
    area    = func(x)
    x[i]=upper_limit
    area += func(x)
    area   *= 0.5
    x[i]    = lower_limit
    for k in range(1,N): # loop over k=1,..,N-1
        x[i]  += h # midpoint value
        area += func(x)
    return area*h

def d2_trapez(lower_limit, upper_limit,N,R=1):
    h=(upper_limit-lower_limit)/N   
    x=[lower_limit,0.]
# F(upper_limit)=F(lower_limit)=0:
    area = 0.
    for k in range(1,N): # loop over k=1,..,N-1
        x[0]  += h # midpoint value
        low = -np.sqrt(R*R-x[0]*x[0])
        up  = -low
        area += int_trapez(low, up,f,x,1,N)
    return area*h        

def mc_nball(N=1000,D=3,R=1):
    """
    Calculates the volume of a hypersphere using accept and reject
    N: Number of random points
    D: Number of dimensions
    R: Radius of hypersphere
    """
    vol=0.
    for _ in range(N):
        r=0.
        for _ in range(D):
            xi=random.uniform(-R,R)
            r+=xi*xi
        if np.sqrt(r) <= R: vol += 1
    print("Number of points inside n-ball: ", vol)
    return vol/N*(2*R)**D

def mc_nball_sampling(N=1000,D=3,R=1):
    """
    Calculates the volume of a hypersphere using sampling
    N: Number of random points
    D: Number of dimensions
    R: Radius of hypersphere
    """
    vol=0.
    x=[0. for i in range(D-1)]
    for _ in range(N):
        for i in range(D-1):
            x[i]=random.uniform(-R,R)
        vol += f(x)
    return vol/N*(2*R)**(D-1)

def nball(R=1,D=3):
    """
    Returns volume of hypersphere
    """
    return (np.pi*R*R)**(D/2)/(gamma(D/2+1))
    
if __name__ == '__main__':
    N=100*100*100
    D=6
    mc=mc_nball(N,D)
    mc2=mc_nball_sampling(N,D)
    an=nball(1,D)
    print(mc, mc2, an, "error=",(mc-an),"error2=",(mc2-an) )

    N=100

    Area = d2_trapez(-1,1,N=N)
    print('Numerical value= ', Area)
    print('Error= ', (an-Area)) # Analytical result is 2
