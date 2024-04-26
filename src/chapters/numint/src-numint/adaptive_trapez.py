#%%
import numpy as np

def g(x):
    return np.exp(3*x)*np.sin(2*x)
# Function to be integrated
def f(x):
    return np.sin(x)
# step size is chosen automatically to reach the specified tolerance 
def trapezoidal_adaptive(f,a,b,EPS=1e-5):
    """
    f   : function to be integrated on the domain [a,b]
    EPS :  accuracy of integral 
    """
    eps=1
    h=(b-a)
    I_old=h*np.sum(0.5*f(a)+0.5*f(b))
    while (np.abs(eps)>EPS):
        h=h/2
        x=np.arange(a+h,b,2*h) # only odd terms
        I_new=I_old/2+h*np.sum(f(x)) # I_old/2 h--> h/2 
        eps=(I_old-I_new)/3
        I_old=I_new
    print('No of steps = ', (b-a)/h)
    return I_new-eps # improvd estimalte 
        
prec=1e-8
a=0
b=np.pi/4
Area = trapezoidal_adaptive(g,a,b,prec)
print('Numerical value = ', Area)
print('Error           = ', (2-Area)) # Analytical result is 2


def int_adaptive_trapez2(lower_limit, upper_limit,func,tol):
    """
    adaptive quadrature, integrate a function from lower_limit
    to upper_limit within tol*(upper_limit-lower_limit)

    """
    S=[]
    S.append([lower_limit,upper_limit])
    I=0
    iterations=0
    while S:
        iterations +=1
        a,b=S.pop(-1) # last element
        m=(b+a)*0.5   # midpoint
        I1=0.5*(b-a)*(func(a)+func(b)) #trapezoidal for 1 interval 
        I2=0.25*(b-a)*(func(a)+func(b)+2*func(m)) #trapezoidal for 2 intervals
        if(np.abs(I1-I2)<3*np.abs((b-a)*tol)):
            I+=I2     # accuarcy met
        else:
            S.append([a,m]) # half the interval 
            S.append([m,b])
    print("Number of iterations: ", iterations)
    return I

Area = int_adaptive_trapez2(a,b,g,prec)
print("trapez 2", Area)
print("error", Area-2)

def simpson_step(a, b,func):
    m=0.5*(a+b)
    return (b-a)/6*(func(a)+func(b)+4*func(m))

def int_adaptive_simpson(func,a, b,tol):
    """
    adaptive quadrature, integrate a function from a
    to b within tol*(b-a) uses simpsons rule
    """
    S=[]
    S.append([a,b])
    I=0
    iterations=0
    while S:
        iterations +=1
        a,b=S.pop(-1) # last element
        m=(b+a)*0.5   # midpoint
        I1=simpson_step(a,b,func) #simpsons for 1 interval 
        I2=simpson_step(a,m,func)+simpson_step(m,b,func) # ...2 intervals
        if(np.abs(I1-I2)<15*np.abs((b-a)*tol)):
            I+=I2     # accuarcy met
        else:
            S.append([a,m]) # half the interval 
            S.append([m,b])
    print("Number of iterations: ", iterations)
    return I

Area = int_adaptive_simpson(g,a,b,prec)
print(Area)
print("error", Area-2)


#%timeit int_adaptive_trapez2(a,b,f,prec)

#%timeit int_adaptive_trapez2(a,b,f,prec)
#%%