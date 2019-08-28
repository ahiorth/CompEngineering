import matplotlib.pyplot as plt
import numpy as np

def f(x):
    return np.sin(x)

def df(x,h):
    return (f(x+h)-f(x))/h

def err(x,h):
    return np.abs(df(x,h)-np.cos(x))
x=0.2
h=1e-8
print(df(x,h), 'error = ', df(x,h)-np.cos(x))
# to generate plot
step_size = [1/(1e1*10**h) for h in range(16)]
error = list(map(err,[x]*len(step_size),step_size))
fig = plt.figure(dpi=150)
plt.loglog(step_size, error, '-o', label='$\sin (x)$')
plt.grid()
plt.xlabel('Step size')
plt.ylabel('Error')
# Save the plot in a file
plt.savefig('df.png', bbox_inches='tight',transparent=True)
plt.show()
