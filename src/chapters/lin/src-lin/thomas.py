import numpy as np

def GJ(A,b):
# Gauss-Jordan Elimination
    for i in range(1,N):
        fact    = A[i:,i-1]/A[i-1,i-1]
        A[i:,] -= np.outer(fact,A[i-1,])
        b[i:]  -= b[i-1]*fact
# Backsubstitution
    sol = np.zeros(N,float)
    sol[N-1]=b[N-1]/A[N-1,N-1]
    for i in range(2,N+1):
        sol[N-i]=(b[N-i]-np.dot(A[(N-i),],sol))/A[N-i,N-i]
return sol
