import numpy as np
import random
import matplotlib.pyplot as plt

def add_dices(no_dic,N):
    sum=np.zeros(6*no_dic+2)
    for k in range(0,N):
        sumi=0
        for dice in range(0,no_dic):
            sumi  += random.randint(1,6)
        sum[sumi] += 1
    return np.arange(len(sum)),sum/N

N=1000000
x,y=add_dices(7,N)
plt.bar(x,y, align='center', alpha=0.5)
plt.show()
