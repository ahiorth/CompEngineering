import numpy as np
# Function to be integrated
def f(x):
    return np.sin(x)
# Gaussian Quadrature for N=2
def int_gaussquad2(func, lower_limit, upper_limit):
    x   = np.array([-1/np.sqrt(3.),1/np.sqrt(3)])
    w   = np.array([1, 1])
    xp  = 0.5*(upper_limit-lower_limit)*x
    xp += 0.5*(upper_limit+lower_limit)
    area = np.sum(w*func(xp))
    return area*0.5*(upper_limit-lower_limit)
                
a=0
b=np.pi
Area = int_gaussquad2(f,a,b)
print('Numerical value = ', Area)
print('Error           = ', (2-Area)) # Analytical result is 2
