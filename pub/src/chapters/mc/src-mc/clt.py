import numpy as np
import random
import matplotlib.pyplot as plt

def average(N):
    x=[np.random.uniform() for _ in range(N)]
    return np.mean(x)

# or alternatively, and equally fast

def average2(N):
    x=0
    for i in range(N):
        x+=np.random.uniform()
    return x/N

def hist(M,N=100):
    y=[average(N) for _ in range(M)]
    plt.hist(x=y, bins='auto', color='#0504aa',alpha=0.7, rwidth=0.85)
    plt.show()

def average3(N):
    x=[np.random.poisson() for _ in range(N)]
    return np.mean(x)

def hist2(M,N=100):
    y=[average3(N) for _ in range(M)]
    plt.hist(x=y, bins='auto', color='#0504aa',alpha=0.7, rwidth=0.85)
    plt.show()

hist2(100000)

import timeit
N=10000000
print( timeit.timeit("average(N)", setup = "from __main__ import average,N", number=1))
print( timeit.timeit("average2(N)", setup = "from __main__ import average2,N", number=1))



