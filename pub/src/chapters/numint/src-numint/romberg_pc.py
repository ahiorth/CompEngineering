import numpy as np
# Function to be integrated
def f(x):
    return np.sin(x)
# step size is choosen automatically to reach (at least) 
# the specified tolerance 
def int_romberg(func, lower_limit, upper_limit,tol,show=False):
    """ calculates the area of func over the domain lower_limit
        to upper limit for the given tol, if show=True the triangular
        array of intermediate results are printed """
    Nmax = 100
    R = np.empty([Nmax,Nmax]) # storage buffer
    h = (upper_limit-lower_limit) # step size
    R[0,0]    =.5*(func(lower_limit)+func(upper_limit))*h
    N = 1
    for i in range(1,Nmax):
        h /= 2
        N *= 2
        odd_terms=0
        for all odd terms 1, 3, ..., N-1 do:
            evaulate function values at odd points,
            sum them and store in odd_terms
        R[i,0]   = 0.5*R[i-1,0] + h*odd_terms

        for all m in 0, 1, ..., i-1:
            R[i,m+1]   = R[i,m] + (R[i,m]-R[i-1,m])/(4**(m+1)-1)                  
	# check tolerance, best guess			
        calc_tol = abs(R[i,i]-R[i-1,i-1])       
        if estimated tolerance calc_tol is lower than tol:
            break  # estimated precision reached
        if max number of iterations are reached (i == Nmax-1):
            print('Romberg routine did not converge after ',
              Nmax, 'iterations!')
            
    if(show==True):
        print out all triangualar elements in R[i,m]

    return R[i,i] #return the best estimate
