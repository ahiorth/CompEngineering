import numpy as np
N=3
lower_limit=0
upper_limit=1
h=(upper_limit-lower_limit)/N
val = [lower_limit+(k+0.5)*h for k in range(N)]
val2 = np.arange(lower_limit+.5*h,upper_limit,h)
print(val)
print(val2)