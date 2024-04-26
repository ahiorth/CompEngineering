import numpy as np
import sympy as sym
import scipy as sc
import scipy.linalg
import scipy.sparse
import scipy.sparse.linalg
n=4
h=1./n
a= -20*1**2/0.72*h*h
w,x,y,z=sym.symbols('w, x, y, z')
f1=sym.Eq(2*x-2*w,a)
f2=sym.Eq(w+y-2*x,a)
f3=sym.Eq(x+z-2*y,a)
f4=sym.Eq(y-2*z,a-25)
sol=sym.solve([f1,f2,f3,f4],(w,x,y,z))
print(sol)

def tri_diag_setup(a, b, c, k1=-1, k2=0, k3=1):
    return np.diag(a, k1) + np.diag(b, k2) + np.diag(c, k3)
a1=np.ones(n-1)
c1=np.ones(n-1)
b1=-np.ones(n)*2
c1[0]=2

A=tri_diag_setup(a1,b1,c1)

d=np.repeat(a,n)
d[n-1]=d[n-1]-25

print(sc.linalg.solve(A,d,))

diagonals=np.zeros((3,n))
diagonals[0,:]= 1                       #all elts in first row is set to 1
diagonals[1,:]= -2  
diagonals[2,:]= 1
diagonals[2,1]= 2
A_sparse = sc.sparse.spdiags(diagonals, [-1,0,1], n, n,format='csc') #sparse matrix instance
