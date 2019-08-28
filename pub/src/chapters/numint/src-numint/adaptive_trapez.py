import numpy as np
# Function to be integrated
def f(x):
    return np.sin(x)
# step size is chosen automatically to reach the specified tolerance 
def int_adaptive_trapez(lower_limit, upper_limit,func,tol):
    N0      = 10
    h       = (upper_limit-lower_limit)/N0
    area    = func(lower_limit)+func(upper_limit)
    area   *= 0.5
    val     = lower_limit
    for k in range(1,N0): # loop over k=1,..,N-1
        val   += h # midpoint value 
        area  += func(val)
    area   *=h
    calc_tol = 2*tol + 1 # just larger than tol to enter the while loop 
    while(calc_tol>tol):
        N = N0*2
        h = (upper_limit-lower_limit)/N
        odd_terms=0
        for k in range (1,N,2): # 1, 3, 5, ... , N-1
            val  = lower_limit + k*h
            odd_terms += func(val)
        new_area = 0.5*area + h*odd_terms
        calc_tol = abs(new_area-area)/3 
        area     = new_area # store new values for next iteration
        N0       = N        # update number of slices
    print('Number of intervals = ', N)
    return area #while loop ended and we can return the area
        
prec=1e-8
a=0
b=np.pi
Area = int_adaptive_trapez(a,b,f,prec)
print('Numerical value = ', Area)
print('Error           = ', (2-Area)) # Analytical result is 2
