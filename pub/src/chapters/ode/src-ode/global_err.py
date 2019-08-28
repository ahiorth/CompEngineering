import numpy as np
def global_err(t,h):
    return np.exp(-t)-(1-h)**(t/h)

print(global_err(10,1e-3))
print(global_err(10,5e-3))
print(global_err(10,10e-3))
print(global_err(10,20e-3))
print(global_err(10,40e-3))
