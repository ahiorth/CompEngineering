#%%
import numpy as np
import matplotlib.pyplot as plt
def f(x):
    return np.sin(x)
def fd(f,x,h):
 """
 calculates the forward difference approximation to 
 the numerical derivative of f in x
 """
 return (f(x+h)-f(x))/h

def fc(f,x,h):
 """
 calculates the central difference approximation to 
 the numerical derivative of f in x
 """
 return 0.5*(f(x+h)-f(x-h))/h

def fdd(f,x,h):
 """
 calculates the numerical second order derivative 
 of f in x
 """
 return (f(x+h)+f(x-h)-2*f(x))/(h*h)
x=1
h=np.logspace(-15,0.1,10)
plt.plot(h,np.abs(np.cos(x)-fd(f,x,h)), '-o',label='forward difference')
plt.plot(h,np.abs(np.cos(x)-fc(f,x,h)),'-x', label='central difference')
plt.plot(h,np.abs(-np.sin(x)-fdd(f,x,h)),'-*',label='second derivative')
plt.grid()
plt.legend()
plt.xscale('log')
plt.yscale('log')
plt.savefig('../fig-taylor/df2_mod.png', bbox_inches='tight',transparent=True)

# %%
