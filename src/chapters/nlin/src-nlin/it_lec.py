#%%
import numpy as np

def g(x):
    return x-x*x+np.exp(-x)

def g2(x):
    return np.exp(-x/2)

x_old=0 # initial guess
for i in range(100):
    x_new=g2(x_old)
    print(x_new)
    if(np.abs(x_old-x_new)<1e-3):
        print('found solution ' + str(x_new) + ' after ' 
        + str(i) + ' iterations')
        break
    else:
        x_old=x_new


# %%
