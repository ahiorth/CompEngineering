
#%%
#%%

import numpy as np
import pandas as pd

my_list  = ['hammer','saw']
my_list2 = ['screw','nail','glue']
new_list = my_list + my_list2
my_list=['hammer', 'saw', 'screw', 'nail', 'glue']
print(my_list[:])      # ['hammer', 'saw', 'screw', 'nail', 'glue']
print(my_list[1:])     # ['saw', 'screw', 'nail', 'glue']
print(my_list[:-1])    # ['hammer', 'saw', 'screw', 'nail']
print(my_list[1:-1])   # ['saw', 'screw', 'nail']
print(my_list[1:-1:2]) # ['saw', 'nail'], picks out every second element
print(my_list[::1])
print(my_list[::2])

my_list=[['hammer','saw'], ['screw','nail','glue']]

finished = False
sum =0
while not finished:
      sum += np.random.random()
      if sum >= 10.:
      	 finished = True
global a
a=2
def f(x):
    global a
    a=10
    b=20
    return a*x+b

def f(a:str,b:int):
    print(a)
    print(b)

#%%
from ctypes import *
so_file = "./square.so"
my_functions = CDLL(so_file)

print(type(my_functions))
print(my_functions.square(4))
# %%

#%%
import numpy as np
x=[3]
def f(y):
    y=y
    y=y.append(1)
    return y
print('x =',x)
print('f(x) returns ', f(x))
print('x is now ', x)

# %%
import numpy as np
x=[3]
def append_to_list(x):
    y=x
    y.append(1)
    return y
print('x = ',x)
print('add_to_list(x) returns ', append_to_list(x))
print('x is now ', x)
#%%
x=[3]
def append_to_np(x):
    x.append(1)
    return x
print('x = ',x)
print('add_to_list(x) returns ', append_to_np(x))
print('x is now ', x)
#%%
x=np.array([3])
def add_to_np(x):
    x=x+3
    return x
def add_to_np2(x):
    x+=3
    return x
print('x = ',x)
print('add_to_np(x) returns ', add_to_np(x))
print('x is now ', x)

print('x = ',x)
print('add_to_np2(x) returns ', add_to_np2(x))
print('x is now ', x)
#%%
N=10000000
x=np.array([3]*N)
%timeit add_to_np(x)
x=np.array([3]*N)
%timeit add_to_np2(x)
#%%
N=1000000
x=[3]*N
%timeit add_to_list(x)
x=np.array([3]*N)
%timeit add_to_np(x)
#print('x = ',x)
#print('f(x) returns ', f(x))
#print('x is now ', x)
#%%
x=np.array([3]*N)
def f(x):
    x=np.append(x,1)
    return x
%timeit f(x)
#print('x = ',x)
#print('f(x) returns ', f(x))
#print('x is now ', x)

# %%
a=np.array([10])
print(id(a))
def f(x):
    print(id(x))
f(a)

# %%
a=[10,12]
def f(x):
    x.append(1)
    return id(x)
print(a)
print(id(a)==f(a)) # False
print(a)
# %%
a=np.array([10])
def f(x):
    x=np.append(x,1) # x=[10,1]
    return id(x)
print(id(a)==f(a)) # False, now a=[10] 

# %%
import numpy as np
def append_to_list(x):
    y=x
    y.append(1)
    return y

def append_to_np(x):
    x=np.append(x,1)
    return x

l=3
N=1000000
x=[3]*N
for i in range(l):
    x.append(3)
%timeit append_to_list(x)
x=np.array([3]*N)
%timeit append_to_np(x)
# %%

# %%
import numpy as np
import matplotlib.pyplot as plt
x_val   = np.linspace(0,1,100) # 100 equal spaced points from 0 to 1
y_vals  = [x_val,x_val*x_val]
labels  = [r'x', r'$x^2$']
cols    = ['r','g']
points  = ['-*','-^']
for y_val,point,col,label in zip(y_vals,points,cols,labels):
    plt.plot(x_val,y_val,point,c=col,label=label)
plt.grid()
plt.legend()
plt.savefig('../fig-python/plt_loop.png',bbox_inches='tight',transparent=True)

plt.show()

# %%
x=[0]*10

# %%
x
# %%
x[0]=1
# %%
x
# %%
x=[[0]*10]
# %%
x
# %%
x[0]=1
x# %%

# %%
