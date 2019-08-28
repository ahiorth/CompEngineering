import numpy as np
# Function to be integrated
def f(x):
    return np.sin(x)
# Gaussian Quadrature for N=3
def int_gaussquad2(lower_limit, upper_limit,func):
    x  = np.array([-np.sqrt(3./5.),0.,np.sqrt(3./5.)])
    w  = np.array([5./9., 8./9., 5./9.])
    xp = 0.5*(upper_limit-lower_limit)*x
    xp += 0.5*(upper_limit+lower_limit)
    area = np.sum(w*func(xp))
    return area*0.5*(upper_limit-lower_limit)
        
        
a=0
b=np.pi
Area = int_gaussquad2(a,b,f)
print('Numerical value = ', Area)
print('Error           = ', (2-Area)) # Analytical result is 2
