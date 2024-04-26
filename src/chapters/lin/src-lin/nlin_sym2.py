#%%
import numpy as np
import sympy as sym


#n=1/2 gives numerical value
#n = sym.Rational(1,2) # gives analytical result
w,x,y,z=sym.symbols('w, x, y, z')
f1=sym.Eq(2*w+x+y+3*z,1)
f2=sym.Eq(w+x+3*y+z,-3)
f3=sym.Eq(w+4*x+y+z,2)
f4=sym.Eq(w+x+2*y+2*z,1)
sol=sym.solve([f1,f2,f3,f4],(w,x,y,z))
print(sol)
f5 = 2*w+x+y+3*z-1
f6 = w+x+3*y+z+3
f7 = w+4*x+y+z-2
f8 = w+x+2*y+2*z-1

f9 = -f5/2+f6
f10 = -f5/2+f7
f11 = -f5/2+f8
print (f9)
print (f10)
print (f11)

f12 = -f9*7+f10
f13 = -f9+f11
print (f12)
print (f13)

f14 = -f12/17+f13
print(f14)
print(sol)
#%%
A = np.array([[2, 1, 1, 3],[1, 1, 3, 1],
              [1, 4, 1, 1],[1, 1, 2, 2 ]],float)
b = np.array([1,-3,2,1],float)
N=4
print(A)
# Gauss-Jordan Elimination
for i in range(1,N):
    fact    = A[i:,i-1]/A[i-1,i-1]
    A[i:,] -= np.outer(fact,A[i-1,])
    b[i:]  -= b[i-1]*fact
print(A)
#%%
A = np.array([[2, 1, 1, 3],[1, 1, 3, 1],
              [1, 4, 1, 1],[1, 1, 2, 2 ]],float)
b = np.array([1,-3,2,1],float)
N=4
print(A)
# Gauss-Jordan Elimination - for loops
for i in range(N):
    for j in range(i+1,N):
        fact    = A[j,i]/A[i,i]
        for k in range(i+1,N):
            A[j,k] = A[j,k]- fact*A[i,k]
        b[j]  = b[j]- b[j-1]*fact
        A[j,i] = 0
print(A)
#%%
# Back substitution
sol = np.zeros(N,float)
sol[N-1]=b[N-1]/A[N-1,N-1]
for i in range(2,N+1):
    sol[N-i]=(b[N-i]-np.dot(A[(N-i),],sol))/A[N-i,N-i]

# Back substitution - for loop
sol = np.zeros(N,float)
for i in range(N-1,-1,-1):
    sol[i]= b[i]
    for j in range(i+1,N):
        sol[i] -= A[i][j]*sol[j]
    sol[i] /= A[i][i]
print(A)
print(b)
print(sol)

sol = np.zeros(N,float)
for i in range(N):
    sol[N-1-i]= b[N-1-i]
    for j in range(i):
        sol[N-1-i] -= A[N-1-i][N-1-j]*sol[N-1-j]
    sol[N-1-i] /= A[N-1-i][N-1-i]
print(A)
print(b)
print(sol)

from numpy.linalg import solve
x=solve(A,b)
#end

# %%
