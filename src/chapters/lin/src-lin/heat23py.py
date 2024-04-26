#%matplotlib inline
import numpy as np
import scipy as sc
import scipy.sparse.linalg
from numpy.linalg import solve
import matplotlib.pyplot as plt

# Set simulation parameters
h = 0.01               # element size
L = 1.0                 # length of domain
n = int(round(L/h)) -1  # number of unknowns, assuming known boundary values
x=np.arange(n+2)*h      # x includes min and max at boundaries were bc are imposed.
T1=25
sigma = 20*L**2/0.72
#Define useful functions

def tri_diag_setup(a, b, c, k1=-1, k2=0, k3=1):
    return np.diag(a, k1) + np.diag(b, k2) + np.diag(c, k3)

def theta_analytical(sigma,x):
    return sigma*(1-x*x)/2+25

#Create matrix for linalg solver
a=np.ones(n-1)/h
b=-np.ones(n)*2/h
c=np.ones(n-1)/h
# no-flux boundary lhs
c[0]=2/h

A=tri_diag_setup(a,b,c)
 
#rhs - constant temperature Finite Volume
da=np.repeat(-h*sigma,n)
da[n-1]=da[n-1]-T1/h

#Create matrix for sparse solver
diagonals=np.zeros((3,n))
diagonals[0,:]= 1/h
diagonals[1,:]= -2/h  
diagonals[2,:]= 1/h

# rhs vector
d=np.repeat(-h*sigma,n)

#----boundary conditions ------
#lhs - no flux of heat
diagonals[1,0]= -1/h 
#rhs - constant temperature Finite Volume
d[n-1]=d[n-1]-2*T1/h
diagonals[1,n-1]= -3/h 
#------------------------------

A_sparse = sc.sparse.spdiags(diagonals, [-1,0,1], n, n,format='csc') 


#Solve linear problems
theta2 = solve(A,da,)
theta  = sc.sparse.linalg.spsolve(A_sparse,d) 
#uncomment to test efficiency
#%timeit sc.sparse.linalg.spsolve(A_sparse,d)
#%timeit solve(A,d,)

# Plot solutions
plt.plot(x[1:-1],theta,x[1:-1],theta2,'-.',x,theta_analytical(sigma,x),':', lw=3)
plt.xlabel("Dimensionless length")
plt.ylabel(r"Temperature [$^\circ$C]")
plt.xlim(0,1)
plt.ylim(T1-1)
plt.legend(['sparse','linalg','analytical'])
plt.grid()
plt.show()
print(theta-theta_analytical(sigma,x[1:-1]))
