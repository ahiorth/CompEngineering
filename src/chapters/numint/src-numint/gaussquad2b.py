import numpy as np
# Function to be integrated
def f(x):
    return x**(1/2)*np.cos(x)
def f2(x):
    return np.cos(x)
def int_gaussquad2b(func):
    x = np.array([0.2899491979256903, 0.8211619131854209])
    w = np.array([0.27755599823106164, 0.38911066843560504])
    area=w*func(x)
    return np.sum(area)
# Gaussian Quadrature for N=3
def int_gaussquad2(lower_limit, upper_limit,func):
    x  = np.array([-np.sqrt(3./5.),0.,np.sqrt(3./5.)])
    w  = np.array([5./9., 8./9., 5./9.])
    xp = 0.5*(upper_limit-lower_limit)*x
    xp += 0.5*(upper_limit+lower_limit)
    area = np.sum(w*func(xp))
    return area*0.5*(upper_limit-lower_limit)
        
        
a=0
b=1
Area = int_gaussquad2(a,b,f)
Area2 = int_gaussquad2b(f2)
print('Numerical value = ', Area)
print('Numerical value = ', Area2)
print('Error           = ', (0.5312026830752897-Area))
print('Error           = ', (0.5312026830752897-Area2))

x = np.array([0.265411702318479, 0.811511374604598])
w = np.array([0.329723879210972, 0.420276120789028])
print(np.sum(w*f2(x)))
