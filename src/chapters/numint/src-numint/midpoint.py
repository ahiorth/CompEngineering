#%%
import numpy as np
# Function to be integrated
def f(x):
    return np.sin(x)

def midpoint(f,a,b,N):
    """
    f : function to be integrated on the domain [a,b]
    N : number of integration points
    """
    h=(b-a)/N
    x=np.arange(a+0.5*h,b,h)
    return h*np.sum(f(x))
N=10
a=0
b=np.pi
Area = midpoint(f,a,b,N)
print('Numerical value= ', Area)
print('Error= ', (2-Area)) # Analytical result is 2
#%%
