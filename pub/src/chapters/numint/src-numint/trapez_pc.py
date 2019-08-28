import numpy as np
# Function to be integrated
def f(x):
    return np.sin(x)

#In the implementation below the calculation goes faster 
#when we avoid unnecessary multiplications by h in the loop
def int_trapez(func, lower_limit, upper_limit,N):
    """ calculates the area of func over the domain lower_limit
        to upper limit using N integration points """
    h       = (upper_limit-lower_limit)/N # step size
    area    = 0.5*(func(lower_limit)+func(upper_limit))
    val     = lower_limit
    for all integration points do:
        estimate integration midpoint value, xi
        add are under curve: func(xi)*h
    return area


