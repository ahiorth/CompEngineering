import numpy as np
from scipy.special import gamma
import random

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
    print(vol)
    return vol/N*(2*R)**D

def nball(R=1):
    """
    Returns volume of hypersphere
    """
    return (np.pi*R*R)**(D/2)/(gamma(D/2+1))
    
if __name__ == '__main__':
    N=100000
    D=12
    mc=mc_nball(N,D)
    an=nball()
    print(mc, an, (mc-an) )
