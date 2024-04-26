import numpy as np

def FluidPotential(r,Q,h):
    phi = Q/(2*np.pi*h)*np.log(r)
    return phi

