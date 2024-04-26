import numpy as np
# Function to be integrated
def f(x):
    return np.sin(x)
#Numerical derivative of function
def df(x,func):
    dh=1e-5 # some low step size
    return (func(x+dh)-func(x))/dh 
#Adaptive midpoint rule, "adaptive" because the number of 
#function evaluations depends on the integrand
def int_adaptive_midpoint(func, lower_limit, upper_limit, tol):
    """ calculates the area of func over the domain lower_limit
        to upper limit for the specified tolerance tol """
    dfa  = df(lower_limit,func) # derivative in point a 
    dfb  = df(upper_limit,func) # derivative in point b
    h    = np.sqrt(abs(24*tol/(dfb-dfa)))
    print('Number of intervals = ', (upper_limit-lower_limit)/h)
    for all integration points do:
        estimate integration midpoint value, xi
        add area under curve: func(xi)*h
    return area 
