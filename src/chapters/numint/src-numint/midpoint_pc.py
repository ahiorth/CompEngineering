import numpy as np
# Function to be integrated
def f(x):
    return np.sin(x)

def int_midpoint(func, lower_limit, upper_limit,N):
    """ calculates the area of func over the domain lower_limit
        to upper limit using N integration points """
    h    = (upper_limit-lower_limit)/N # step size 
    area = 0.
    for all integration points do:
        estimate integration midpoint value, xi
        add area under curve: func(xi)*h
    return area 
