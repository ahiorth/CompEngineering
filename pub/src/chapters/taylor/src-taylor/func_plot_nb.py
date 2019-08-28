import matplotlib.pyplot as plt
import numpy as np

x=np.arange(-np.pi,np.pi,1)

f = np.sin(x)
plt.plot(x,f)
plt.grid()

plt.show()


