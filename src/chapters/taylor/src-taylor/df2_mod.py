#%%
import numpy as np
import matplotlib.pyplot as plt
def f(x):
    return np.sin(x)
def fd(f,x,h):
    """ f'(x) forward difference """
    return (f(x+h)-f(x))/h

def fc(f,x,h):
    """ f'(x) central difference """
    return 0.5*(f(x+h)-f(x-h))/h

def fdd(f,x,h):
    """ f''(x) second order derivative """
    return (f(x+h)+f(x-h)-2*f(x))/(h*h)

def fd3(f,x,h):
    """ f'''(x) third order derivative """
    return (2*f(x-h)-2*f(x+h)-f(x-2*h)+f(x+2*h))/(2*h*h*h)

def fd_4(f,x,h):
    """ f'(x) fourth order """
    return (8*f(x+h)-8*f(x-h)-f(x+2*h)+f(x-2*h))/(12*h)
x=1
h=np.logspace(-15,0.1,10)
plt.plot(h,np.abs(np.cos(x)-fd(f,x,h)), '-o',label='forward difference')
plt.plot(h,np.abs(np.cos(x)-fc(f,x,h)),'-x', label='central difference')
plt.plot(h,np.abs(np.cos(x)-fd_4(f,x,h)),'-*',label='derivative - fourth order')
plt.plot(h,np.abs(-np.sin(x)-fdd(f,x,h)),'-*',label='second derivative')
h=np.logspace(-7,0.1,10)
plt.plot(h,np.abs(-np.cos(x)-fd3(f,x,h)),'-*',label='third derivative')

plt.grid()
plt.legend()
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Step size $h$')
plt.ylabel('Numerical error')
plt.savefig('../fig-taylor/df2_mod.png', bbox_inches='tight',transparent=True)

# %%
