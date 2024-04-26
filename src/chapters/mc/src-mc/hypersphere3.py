from scipy.special import gamma
import numpy as np

def f(x,R=1):
    r=R*R
    for xi in x:
      r-=xi*xi
    if(r<0):
        return 0.
    else:
        return 2*np.sqrt(r)

def d1_trapez(lower_limit, upper_limit,func,x,i,N):
    h     = (upper_limit-lower_limit)/N
    x[i]  = lower_limit
    area  = func(x)
    x[i]  = upper_limit
    area += func(x)
    area *= 0.5
    x[i]  = lower_limit
    for k in range(1,N): # loop over k=1,..,N-1
        x[i]  += h # midpoint value
        area  += func(x)
    return area*h

def d2_trapez(lower_limit, upper_limit,func,x,i,N):
    h     = (upper_limit-lower_limit)/N
    x[i]  = lower_limit
    area  = d1_trapez(lower_limit, upper_limit,func,x,i+1,N)
    x[i]  = upper_limit
    area += d1_trapez(lower_limit, upper_limit,func,x,i+1,N)
    area *= 0.5
    x[i]  = lower_limit
    for k in range(1,N): # loop over k=1,..,N-1
        x[i] += h # midpoint value
        area += d1_trapez(lower_limit, upper_limit,func,x,i+1,N)
    return area*h        

def d3_trapez(lower_limit, upper_limit,func,x,i,N):
    h     = (upper_limit-lower_limit)/N
    x[i]  = lower_limit
    area  = d2_trapez(lower_limit, upper_limit,func,x,i+1,N)
    x[i]  = upper_limit
    area += d2_trapez(lower_limit, upper_limit,func,x,i+1,N)
    area *= 0.5
    x[i]  = lower_limit
    for k in range(1,N): # loop over k=1,..,N-1
        x[i] += h # midpoint value
        area += d2_trapez(lower_limit, upper_limit,func,x,i+1,N)
    return area*h

def mc_nball(N=1000,D=3,R=1):
    """
    Calculates the volume of a hypersphere using accept and reject
    N: Number of random points
    D: Number of dimensions
    R: Radius of hypersphere
    """
    vol=0.
    for k in range(N):
        r=0.
        for d in range(D):
            xi=np.random.uniform(-R,R)
            r+=xi*xi
        if np.sqrt(r) <= R: vol += 1
    print("Number of points inside n-ball: ", vol)
    return vol/N*(2*R)**D

def mc_nballII(N=1000,D=3,R=1):
    """
    Calculates the volume of a hypersphere using accept and reject
    N: Number of random points
    D: Number of dimensions
    R: Radius of hypersphere
    """
    r=0
    for d in range(D):
        xi=np.random.uniform(-R,R,size=N)
        r+=xi*xi
    r=np.sqrt(r)
    vol = np.sum(r<=R)
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
            x[i]=np.random.uniform(-R,R)
        vol += f(x)
    return vol/N*(2*R)**(D-1)

def nball(R=1,D=3):
    """
    Returns volume of hypersphere
    """
    return (np.pi*R*R)**(D/2)/(gamma(D/2+1))
    
if __name__ == '__main__':
    import timeit
    n=100
    D=4
    N=1000000
    n= int(N**(1/D))
    mc=mc_nball(N,D)
    an=nball(1,D)
    print(mc, an, "error=",(mc-an) )
    mc=mc_nballII(N,D)
    an=nball(1,D)
    print(mc, an, "errorII=",(mc-an) )
    
    mc=mc_nball_sampling(N,D)
    an=nball(1,D)
    print(mc, an, "errorII=",(mc-an) )


    n=100;D=3
    x = [0. for i in range(D)]
    volume=d3_trapez(-1,1,f,x,0,N=n)
    print("volume of hyperspher in 4D: ", volume)
   
    print('Numerical value= ', volume)
    print('Error= ', (an-volume))

    n=12;D=3
    an=nball(1,D)
    x = [0. for i in range(D)]
    volume=d2_trapez(-1,1,f,x,0,N=n)
    print("volume of hyperspher in 3D: ", an)
   
    print('Numerical value= ', volume)
    print('Error= ', (an-volume))
