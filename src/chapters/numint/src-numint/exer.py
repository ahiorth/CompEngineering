import numpy as np
from scipy import integrate
# Function to be integrated
def f(x):
    return x**(1/3)*np.cos(x)
#def f(x):
#    return 3*x**3*np.cos(x**3)
def f(x):
    return np.sin(x)
def f(x):
    return x*x*x*x
def f(x):
    return x**(1/2)*np.cos(x)
#def f(x):
#    return 2*x**2*np.cos(x**2)
#def f(x):
#    return x**(1/2)*np.log(x)
#def f(x):
#    return np.exp(-x*x)
#Numerical derivative of function
def df(x,func):
    dh=1e-5 # some low step size
    return (func(x+dh)-func(x))/dh 

def int_trapez(lower_limit, upper_limit,func,N):
    """ calculates the area of func over the domain lower_limit
        to upper limit using N integration points """
    h       = (upper_limit-lower_limit)/N
    area    = func(lower_limit)+func(upper_limit)
    area   *= 0.5
    val     = lower_limit
    for k in range(1,N): # loop over k=1,..,N-1
        val  += h # midpoint value 
        area += func(val)
    return area*h

#Adaptive midpoint rule, "adaptive" because the number of 
#function evaluations depends on the integrand
def int_adaptive_midpoint(lower_limit, upper_limit,func,tol):
    dfa  = df(lower_limit,func) # derivative in point a 
    dfb  = df(upper_limit,func) # derivative in point b
    N    = abs((upper_limit-lower_limit)**2*(dfb-dfa)/24/tol)
    N    = int(np.sqrt(N)) + 1  # +1 as int rounds down
    h    = (upper_limit-lower_limit)/N
    area = 0.
    print('Number of intervals = ', N)
    for k in range(0,N): # loop over k=0,1,..,N-1
        val = lower_limit+(k+0.5)*h # midpoint value 
        area += func(val)
    return area*h

#Adaptive midpoint rule, "adaptive" because the number of 
#function evaluations depends on the integrand
def int_adaptive_trapez(lower_limit, upper_limit,func,tol):
    dfa  = df(lower_limit,func) # derivative in point a 
    dfb  = df(upper_limit,func) # derivative in point b
    N    = abs((upper_limit-lower_limit)**2*(dfb-dfa)/24/tol)
    N    = int(np.sqrt(N)) + 1  # +1 as int rounds down
    h       = (upper_limit-lower_limit)/N
    print('Number of intervals = ', N)
    area    = func(lower_limit)+func(upper_limit)
    area   *= 0.5
    val     = lower_limit
    for k in range(1,N): # loop over k=1,..,N-1
        val  += h # midpoint value 
        area += func(val)
    return area*h

# step size is chosen automatically to reach the specified tolerance 
def int_adaptive_trapez2(lower_limit, upper_limit,func,tol):
    N0      = 1
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

def int_romberg(lower_limit, upper_limit,func,tol):
    Nmax = 100
    R = np.empty([Nmax,Nmax]) # storage buffer
    R[0,0]    =.5*(func(lower_limit)+func(upper_limit))*(upper_limit-lower_limit)
    N         = 1
    for i in range(1,Nmax):
        N = N*2
        h = (upper_limit-lower_limit)/N
        odd_terms=0
        for k in range (1,N,2): # 1, 3, 5, ... , N-1
            val        = lower_limit + k*h
            odd_terms += func(val)
		# add the odd terms to the previous estimate	
        R[i,0]   = 0.5*R[i-1,0] + h*odd_terms 
        for m in range(0,i): # m = 0, 1, ..., i-1# add all higher order terms in h
            R[i,m+1]   = R[i,m] + (R[i,m]-R[i-1,m])/(4**(m+1)-1)                  
		# check tolerance, best guess			
        calc_tol = abs(R[i,i]-R[i-1,i-1])
        if(calc_tol<tol):
            break  # estimated precision reached 
    if(i == Nmax-1):
        print('Romberg routine did not converge after ',
              Nmax, 'iterations!')
    else:      
        print('Number of intervals = ', N)

    elem = [2**idx for idx in range(i+1)]
    print("Steps StepSize Results")
    for idx in range(i+1):
        print(elem[idx],' ',"{:.6f}".format((upper_limit-lower_limit)/2**idx),end = ' ')
        for l in range(idx+1):
            print("{:.6f}".format(R[idx,l]),end = ' ')
        print('')
    return R[i,i] #while loop ended and we can return the best estimate

def int_gaussquad2(lower_limit, upper_limit,func):
    N=3
    x = [-np.sqrt(3./5.),0.,np.sqrt(3./5.)]
    w = [5./9., 8./9., 5./9.]
    area = 0.
    for i in range(0,N):
        xp = 0.5*(upper_limit-lower_limit)*x[i]
        xp+= 0.5*(upper_limit+lower_limit)
        area += w[i]*func(xp)
    return area*0.5*(upper_limit-lower_limit)

prec=1e-9
a=1e-8
b=2
b=np.pi**0.5
b=np.pi
#a=-1
b=1
Area = int_adaptive_midpoint(a,b,f,prec)
Area2 = int_adaptive_trapez(a,b,f,prec)
Area3 = int_adaptive_trapez2(a,b,f,prec)
Area4 = int_romberg(a,b,f,prec)
Area5 = integrate.romberg(f, a, b, show=True)
Area6 = int_gaussquad2(a,b,f)
Ana = 0.6076257393
Ana = 0.5312026830
print('Numerical value = ', Area)
print('Numerical value = ', Area2)
print('Numerical value = ', Area3)
print('Numerical value, Romberg = ', Area4)
print('Numerical value, Gauss = ', Area6)
print('Error           = ', (Area-Ana)) # Analytical result is 2
print('Error           = ', (Area2-Ana)) # Analytical result is 2
print('Error           = ', (Area3-Ana)) # Analytical result is 2
print('Error, Romberg  = ', (Area4-Ana)) # Analytical result is 2
print('Error, SciPy    = ', (Area5-Ana)) # Analytical result is 2
print('Error, Gauss    = ', (Area6-Ana)) # Analytical result is 2
