#%%
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
import scipy.sparse.linalg
from numba import jit

central_difference=True
# set simulation parameters
h=0.0025
L=1.0
n = int(round(L/h))
Tb=25 #rhs
sigma=100
k=1.65 
beta = sigma*L**2/k

y = np.arange(n+1)*h

def analytical(x):
    return beta*(1-x*x)/2+Tb
def tri_diag(a, b, c, k1=-1, k2=0, k3=1):
    """ a,b,c diagonal terms
        default k-values for 4x4 matrix:
        | b0 c0 0  0 |
        | a0 b1 c1 0 |
        | 0  a1 b2 c2|
        | 0  0  a2 b3|
    """
    return np.diag(a, k1) + np.diag(b, k2) + np.diag(c, k3)

# just-in-time (jit) compiler from numba, to speed up the loop in the TDMA solver
# If this line gives you trouble, then you can either
# install numba (recommended) or you can comment it out
@jit(nopython = True)
def tdma_solver(a, b, c, d):
    # Solves Ax = d,
    # where layout of matrix A is
    # b1 c1 ......... 0
    # a2 b2 c2 ........
    # .. a3 b3 c3 .....
    # .................
    # .............. cN-1
    # 0 ..........aN bN
    # Note index offset of a
    N = len(d)
    c_ = np.zeros(N-1)
    d_ = np.zeros(N)
    x  = np.zeros(N)
    c_[0] = c[0]/b[0]
    d_[0] = d[0]/b[0]
    for i in range(1, N-1):
        c_[i] = c[i]/(b[i] - a[i-1]*c_[i-1])
    for i in range(1, N):
        d_[i] = (d[i] - a[i-1]*d_[i-1])/(b[i] - a[i-1]*c_[i-1])
    x[-1] = d_[-1]
    for i in range(N-2, -1, -1):
        x[i] = d_[i] - c_[i]*x[i+1]
    return x

def tdma(A, b):
    # Solves Ax = b to find x
    # This is a wrapper function, which unpacks
    # A from a sparse diagonal matrix structure into separate diagonals,
    # and pass them to the numba-compiled solver defined above.
    # Note, this method needs A to be diagonally dominant
    # (which it will be, for this problem)
    x = tdma_solver(A.diagonal(-1), A.diagonal(0), A.diagonal(1), b)
    return x

#Create matrix for sparse solver
diagonals=np.zeros((3,n))
diagonals[0,:]= 1
diagonals[1,:]= -2  
diagonals[2,:]= 1

a=np.ones(n-1)
b=-2*np.ones(n)
c=np.ones(n-1)
#lhs boundary condition
if central_difference:
    c[0]=2
    diagonals[2,1]= 2
else:
    b[0]=-1
    diagonals[1,0]= -1

A=tri_diag(a,b,c)
A_sparse = sc.sparse.spdiags(diagonals, [-1,0,1], n, n,format='csc') 
# to view matrix
#print(A_sparse.todense())
#rhs vector
d=np.repeat(-h*h*beta,n)
#rhs boundary condition
d[-1]=d[-1]-Tb
Tn=np.linalg.solve(A,d)
Tns = sc.sparse.linalg.spsolve(A_sparse,d)
Tns2=tdma(A,d)
#append boundary temperature
Tn=np.append(Tn,Tb)
Tns=np.append(Tns,Tb)
Tns2=np.append(Tns2,Tb)
#analytical solution
ya=np.arange(0,1,0.01)
Ta=analytical(ya)
#view 
if central_difference:
    plt.title('Central Difference Formulation')
else:
    plt.title('Forward Difference Formulation')
plt.plot(ya,Ta,label='analytical')
plt.plot(y,Tn,'*',label='numerical')
plt.plot(y,Tns,'*',label='numerical-sparse')
plt.plot(y,Tns2,'*',label='numerical-tdma')
plt.legend()
plt.grid()
ni=n//2
yi=y[ni]
err=np.abs(Tn[ni]-analytical(yi))
print('error at point ' + str(ni)+' is='+str(err))

%timeit sc.sparse.linalg.spsolve(A_sparse,d)
%timeit np.linalg.solve(A,d)
%timeit tdma(A,d)
# %%
