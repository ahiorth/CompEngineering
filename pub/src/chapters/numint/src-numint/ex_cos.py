import numpy as np
import matplotlib.pyplot as plt

x=np.arange(0,1,1e-3)
f = x**(1/3)*np.cos(x)

plt.plot(x,f)
plt.show()
