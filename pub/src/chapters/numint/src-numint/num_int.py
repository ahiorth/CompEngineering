import numpy as np
import matplotlib.pyplot as pl
import scipy.integrate as integrate
# Function to be integrated
def f(x):
    return np.exp(x**2)
    
def int_trapez(lower_limit, upper_limit,func,N):
    delta_x = (upper_limit-lower_limit)/N
    area    = func(lower_limit)+func(upper_limit)
    area   *= 0.5
    val     = lower_limit
    for k in range(1,N): # loop over k=1,..,N-1
        val  += delta_x # midpoint value 
        area += func(val)
    return area*delta_x

def int_rect(lower_limit, upper_limit,func,N):
    delta_x=(upper_limit-lower_limit)/N
    area=0.
    for k in range(0,N): # loop over k=0,1,..,N-1
        val = lower_limit+(k+0.5)*delta_x # midpoint value 
        area += func(val)*delta_x
    return area

a = 0
b = 5
N = 5
x=np.arange(a,b,0.01)

Ana1 = integrate.quad(f, a, b)
Ana=Ana1[0]
print(Ana/(np.exp(b)-np.exp(a)))
Box    = int_rect(a,b,f,N)
Trapez = int_trapez(a,b,f,N)
print('box= ', Box, 'Error= ',2*abs(Box-Ana)/(Ana+Box) , 'trapez= ', Trapez, 'Error= ', 2*abs(Trapez-Ana)/(Ana+Trapez))
print(Ana)

#print(Area)
#pl.plot(x,f(x))
#pl.show()
