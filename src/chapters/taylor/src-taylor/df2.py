#%%
import matplotlib.pyplot as plt
import numpy as np

def f(x):
    return np.sin(x)

def df0(x,h):
    return (f(x+h)-f(x))/(h)

def df(x,h):
    return (f(x+h)-f(x-h))/(2*h)

def df2(x,h):
    return (f(x+h)+f(x-h)-2*f(x))/(h*h)

def err0(x,h):
    return np.abs(df0(x,h)-np.cos(x))

def err(x,h):
    return np.abs(df(x,h)-np.cos(x))

def err2(x,h):
    return np.abs(df2(x,h)+np.sin(x))
x=0.2
h=1e-8
print(df(x,h), 'error = ', df(x,h)-np.cos(x))
# to generate plot
step_size = [1/(1e1*10**h) for h in range(16)]
err0 = list(map(err0,[x]*len(step_size),step_size))
err = list(map(err,[x]*len(step_size),step_size))
errb = list(map(err2,[x]*len(step_size),step_size))

fig = plt.figure()
plt.loglog(step_size, err0, '-o', label='Forward Difference')
plt.loglog(step_size, err, '-x', label='Sentral Difference')
plt.loglog(step_size, errb, '-*', label='$f^{\prime\prime}(x)$')
plt.grid()
plt.xlabel('Step size')
plt.ylabel('Error')
# Save the plot in a file
plt.legend()
plt.savefig('df2.png', bbox_inches='tight',transparent=True)
plt.show()

# %%
