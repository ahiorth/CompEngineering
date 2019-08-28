import numpy as np
# Function to be integrated
def f(x):
    return np.sin(x)
# step size is chosen automatically to reach the specified tolerance 
def int_adaptive_trapez(func, lower_limit, upper_limit, tol):
    """ calculates the area of func over the domain lower_limit
        to upper limit for the specified tolerance tol """
    h       = (upper_limit-lower_limit)
    area    = 0.5*(func(lower_limit)+func(upper_limit))
    calc_tol = tol + 1 # just larger than tol to enter the while loop 
    while(calc_tol>tol):
        half the step size h /= 2
        for all odd integration points in the domain:
            sum up all the odd function values in odd_terms
        new_area = 0.5*area + h*odd_terms
        calc_tol = abs(new_area-area)/3 
        area     = new_area # store new values for next iteration
    print('Number of intervals = ', (upper_limit-lower_limit)/h)
    return area #while loop ended and we can return the area


