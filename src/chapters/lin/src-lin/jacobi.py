#%%
import numpy as np

def solve_jacobi(A,b,x=-1,w=1,max_iter=1000,EPS=1e-6):
    """
    Solves the linear system Ax=b using the jacobi method, stops if
    solution is not found after max_iter or if solution changes less 
    than EPS
    """
    if(x==-1): #default guess 
        x=np.zeros(len(b))
    D=np.diag(A)
    R=A-np.diag(D)
    eps=1
    x_old=x
    iter=0
    w=0.1
    while(eps>EPS and iter<max_iter):
        iter+=1
        x=w*(b-np.dot(R,x_old))/D + (1-w)*x_old
        eps=np.sum(np.abs(x-x_old))
        print(eps)
        x_old=x
    print('found solution after ' + str(iter) +' iterations')
    return x

def solve_GS(A,b,x=-1,max_iter=1000,EPS=1e-6):
    """
    Solves the linear system Ax=b using the Gauss-Seidel method, stops if
    solution is not found after max_iter or if solution changes less 
    than EPS
    """
    if(x==-1):
        x=np.zeros(len(b))
    D=np.diag(A)
    R=A-np.diag(D)
    eps=1
    iter=0
    while(eps>EPS and iter<max_iter):
        iter+=1
        eps=0.
        for i in range(len(x)):
            tmp=x[i]
            x[i]=(b[i]- np.dot(R[i,:],x))/D[i]
            eps+=np.abs(tmp-x[i])
    print('found solution after ' + str(iter) +' iterations')
    return x

A = np.array([[10, -1, 2,0],[-1, 11, -1,3],
              [2, -1, 10, -1],[0, 3, -1, 8 ]],float)
b = np.array([6,25,-11,15],float)
print(A)
s1=solve_jacobi(A,b)
print(s1)

A = np.array([[2, 1, 1, 3],[1, 1, 3, 1],
              [1, 4, 1, 1],[1, 1, 2, 2 ]],float)
b = np.array([1,-3,2,1],float)

s2=solve_jacobi(A,b,w=0.01)
print(s2)

s2b=solve_GS(A,b)
print(s2b)
#exchange row 3 and 4, and put w=0.1
A = np.array([[2, 1, 1, 3,],[1, 4, 1, 1, ],
              [1, 1, 3, 1],[1, 1, 2, 2 ]],float)
b = np.array([1,2,-3,1],float)
s3=solve_jacobi(A,b,w=0.1)
print(s3)

s3b=solve_GS(A,b)
print(s3b)
# %%
