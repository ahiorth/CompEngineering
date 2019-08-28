import numpy as np

def sum1(N):
    """ sum integers up to N
        C-type implementation """
    sum = 0.
    for i in range(N+1): # 0, 1, ..., N
        sum += i
    return sum

def sum2(N):
    """ sum integers up to N
        build in Python functions """
    x = [i for i in range(N+1)]
    return sum(x)

def sum3(N):
    """ sum integers up to N
        NumPy functions """
    x = np.arange(N+1)
    return np.sum(x)

N=100
%timeit sum1(N)
%timeit sum2(N)
%timeit sum3(N)
#end

