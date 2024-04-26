import numpy as np
import scipy as sc
import scipy.linalg
import scipy.sparse
import scipy.sparse.linalg
import time
from math import sinh

#import matplotlib.pyplot as plt
from matplotlib.pyplot import *
# Change some default values to make plots more readable on the screen
LNWDT=3; FNT=20
matplotlib.rcParams['lines.linewidth'] = LNWDT; matplotlib.rcParams['font.size'] = FNT

# Set simulation parameters
beta = 5.0
h = 0.1               # element size
L =1.0                  # length of domain
n = int(round(L/h)) -1  # number of unknowns, assuming known boundary values
x=np.arange(n+2)*h      # x includes min and max at boundaries were bc are imposed.


#Define useful functions

def tri_diag_setup(a, b, c, k1=-1, k2=0, k3=1):
    return np.diag(a, k1) + np.diag(b, k2) + np.diag(c, k3)

def theta_analytical(beta,x):
    return np.sinh(beta*x)/np.sinh(beta)

#Create matrix for linalg solver
a=np.ones(n-1)
b=-np.ones(n)*(2+(beta*h)**2)
c=a
A=tri_diag_setup(a,b,c)

#Create matrix for sparse solver
diagonals=np.zeros((3,n))
diagonals[0,:]= 1                       #all elts in first row is set to 1
diagonals[1,:]= -(2+(beta*h)**2)  
diagonals[2,:]= 1 
A_sparse = sc.sparse.spdiags(diagonals, [-1,0,1], n, n,format='csc') #sparse matrix instance

#Crete rhs array
d=np.zeros(n)
d[n-1]=-1

#Solve linear problems
tic=time.clock()
theta = sc.sparse.linalg.spsolve(A_sparse,d) #theta=sc.linalg.solve_triangular(A,d)
toc=time.clock()
print ('sparse solver time:',toc-tic)

tic=time.clock()
theta2=sc.linalg.solve(A,d,)
toc=time.clock()
print ('linalg solver time:',toc-tic)

# Plot solutions
plot(x[1:-1],theta,x[1:-1],theta2,'-.',x,theta_analytical(beta,x),':')
legend(['sparse','linalg','analytical'])
show()
close()
print ('done')
