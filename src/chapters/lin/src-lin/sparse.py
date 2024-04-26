#%%
from numba import njit
from numba.typed import List
import numpy as np
N=10
A=np.zeros(N*N)
A[np.random.randint(0,N*N,size=3*N)]=np.random.randint(-2,2,size=3*N)
A=A.reshape(N,N) # create NxN matrix with a lot of zeros
print(A)

def create_sparse_from_dense(A):
    '''
    Create a sparse matrix from 
    '''
    Ncol=len(A[0,:])
    Nrow=len(A[:,0])
    Asparse=[]
    for i in range(Nrow):
        row=[]
        for j in range(Ncol):
            if(np.abs(A[i][j]) > 0):
                row.append([j,A[i][j]])
        Asparse.append(row)
# convert to numpy array
#    Anp=np.empty(Nrow) 
    y=[]
    for i in range(Nrow):
       y.append(np.array([np.array(xi) for xi in Asparse[i]],dtype=float))

    return np.asarray(y) 

#
#@njit
#
@jit(nopython=True)
def mydot(Asparse,x):
    ret=np.zeros(len(x))
    for i in range(len(Asparse)):
        for j in range(len(Asparse[i])):
            idx=int(Asparse[i][j][0])
            ret[i] += Asparse[i][j][1]*x[idx]
    return ret
x=np.repeat(1,N)
print(np.dot(A,x))

A2=create_sparse_from_dense(A)
print(A2)
print(mydot(A2,x))

#%timeit mydot(A2,x)
#%timeit np.dot(A,x)

V=[ 10, 20, 30, 40, 50, 60, 70, 80]
COL_INDEX = [  0,  1,  1,  3,  2,  3,  4,  5 ]   
ROW_INDEX = [  0,  2,  4,  7,  8 ]

row=1
row_start = ROW_INDEX[row]
row_end   = ROW_INDEX[row + 1]
print(V[row_start:row_end])
print(COL_INDEX[row_start:row_end])
# %%
