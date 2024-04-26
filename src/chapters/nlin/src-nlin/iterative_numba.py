#%%
import numpy as np
from numpy.linalg import solve
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from numba import jit


def iterative(g,x,MAX_ITER=200,EPS=1e-16):
    n=0
    eps=1
    while eps>EPS and n < MAX_ITER:
        x_next = g(x)
        eps = np.abs(x-x_next)
        x = x_next
        n += 1
    return x

#def bisection(f,a,b):
@jit(nopython=True)  
def f(x):
    return x*x-np.exp(-x)
@jit(nopython=True)
def df(x):
    return 2*x+np.exp(-x)

@jit(nopython=True)
def g(x):
    return x-x*x+np.exp(-x)

def g2(x):
    return np.exp(-x/2)

@jit(nopython=True)
def iterative2(x,MAX_ITER=200,EPS=1e-8):
    n=0
    eps=1
    while eps>EPS and n < MAX_ITER:
        x_next = g(x)
        eps = np.abs(x-x_next)
        x = x_next
        n += 1
    return x
#@jit(nopython=True)
def newton(x,f,df, MAX_ITER=50,EPS=1e-8):
    n=0
    eps=1
    while eps >EPS and n < MAX_ITER:
        x_next=x-f(x)/df(x)
        eps=np.abs(x-x_next)
        x=x_next
        n+=1
    return x

if __name__ == "__main__":
    
    
    print("Scipy solver : " +str(fsolve(f, 0)))
    print("My solver 1: " +str(iterative(g, 0)))
    print("My solver 2: " +str(iterative(g2, 0)))
    
    print("My solver 1: " +str(iterative2(0)))
    print("My solver 2: " +str(iterative2(0)))
    print("My solver Newton: " +str(newton(0,f,df)))
    

    


# %%
