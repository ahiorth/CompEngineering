#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

my_variable=0

my_float = 2.0
my_int   = 3
my_bool  = True
my_float = 2.0 
my_int   = 3
my_bool  = True
print(type(my_float))
print(type(my_int))
print(type(my_int))
type(my_float)
type(my_int)
type(my_bool)
#isinstance(my_float)
print(type(my_float))
print(type(my_int))
print(type(my_int))

if isinstance(my_int,int):
    print('My variable is integer')
else:
    print('My variable is not integer')

numbers=['one','two','three','one','two']
result=[]
for number in numbers:
    if number == 'one':
       result.append(1)
numbers  = ['one','two','three','one','two']
numerics = [  1  ,  2  ,   3   , 1   , 2   ]
result=[] # has to be declared as empty
for idx,number in enumerate(numbers):
    if number == 'one':
       result.append(numerics[idx]) 
x_val   = np.linspace(0,1,100)
y_vals  = [x_val,x_val*x_val]
labels  = [r'x', r'$x^2$']
cols    = ['r','g']
points  = ['-*','-^']
for idx,y_val in enumerate(y_vals):
    plt.plot(x_val,y_val,points[idx],c=cols[idx],label=labels[idx])
plt.grid()
plt.legend()
plt.show()

# %%
