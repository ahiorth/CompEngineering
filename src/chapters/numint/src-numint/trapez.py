#%%
import numpy as np
# Function to be integrated
def f(x):
    return np.sin(x)

def trapezoidal(f,a,b,N):
    """
    f : function to be integrated on the domain [a,b]
    N : number of integration points
    """
    h=(b-a)/N
    x=np.arange(a+h,b,h)
    return h*(0.5*f(a)+0.5*f(b)+np.sum(f(x)))
N=10
a=0
b=np.pi
Area = trapezoidal(f,a,b,N)
print('Numerical value= ', Area)
print('Error= ', (2-Area)) # Analytical result is 2
print('Theoretical Error', np.pi**2/6/N/N) 

# %%
