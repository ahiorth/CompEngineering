#%%
import numpy as np
# Function to be integrated
def f(x):
    return np.sin(x)
# step size is choosen automatically to reach (at least) 
# the specified tolerance 
def int_romberg(func,a, b,tol,show=False):
    """ calculates the area of func on the domain [a,b]
        given tol, if show=True the triangular
        array of intermediate results are printed """
    Nmax = 100
    R = np.empty([Nmax,Nmax]) # storage buffer
    h = (b-a) # step size
    R[0,0]    =.5*(func(a)+func(b))*h
    N = 1
    for i in range(1,Nmax):
        h /= 2
        N *= 2
        x=np.arange(a+h,b,2*h)
		# add the odd terms to the previous estimate	
        R[i,0]   = 0.5*R[i-1,0] + h*np.sum(f(x)) 
        for m in range(0,i): # m = 0, 1, ..., i-1
			# add all higher order terms in h
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

    if(show==True):
        elem = [2**idx for idx in range(i+1)]
        print("Steps StepSize Results")
        for idx in range(i+1):
            print(elem[idx],' ',
                  "{:.6f}".format((b-a)/2**idx),end = ' ')
            for l in range(idx+1):
                print("{:.6f}".format(R[idx,l]),end = ' ')
            print('')  
    return R[i,i] #return the best estimate
#end        
prec=1e-8
a=0
b=np.pi
Area = int_romberg(f,a,b,prec,show=True)
print('Numerical value = ', Area)
print('Error           = ', (2-Area)) # Analytical result is 2

from scipy import integrate
integrate.romberg(f, a, b, show=True)

def g(x):
    u=(1-x)
    u*=u
    return np.exp(-x*x/u)/u

w=100
def h(x):
    u=x/(1-x)
    return u*np.exp(-u)*np.cos(w*u)/(1-x)/(1-x)

Area = int_romberg(g,0.,0.99999999,prec,show=True)
print('Numerical value = ', Area)
print('Error           = ', (np.sqrt(np.pi)/2-Area)) # Analytical result is 2

Area = int_romberg(h,0.,0.99999999,prec,show=True)
print('Numerical value = ', Area)
print('Error           = ', ((1-w*w)/(w**2+1)**2-Area)) # Analytical result is 2

integrate.romberg(h, 0, 0.99999999999, show=True)

def i(x):
    return x**4-2*x+1

int_romberg(i,0.,2,prec,show=True)

# %%
