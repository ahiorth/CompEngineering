from scipy.special import gamma
import numpy as np

def mc_nball(N=1000,D=3,R=1):
    """
    Calculates the volume of a hypersphere using accept and reject
    N: Number of random points
    D: Number of dimensions
    R: Radius of hypersphere
    """
    vol=0.
    for _ in range(N):
        xi = np.random.uniform(-R,R,size=D)
        r=np.sum(xi*xi)
        if np.sqrt(r) <= R: vol += 1
#    print("Number of points inside n-ball: ", vol)
    return vol/N*(2*R)**D


def nball(R=1,D=3):
    """
    Returns volume of hypersphere
    """
    return (np.pi*R*R)**(D/2)/(gamma(D/2+1))


if __name__ == '__main__':
    N=100000
    print('D\tanalytical\tMC\tError')
    for D in range(3,10):
        mc=mc_nball(N,D)
        an=nball(1,D)
        print(D,an,mc,mc-an)
    
