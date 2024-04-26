#%%
import numpy as np
import matplotlib.pyplot as plt

central_difference=False
# set simulation parameters
h=0.25
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

a=np.ones(n-1)
b=-2*np.ones(n)
c=np.ones(n-1)
#lhs boundary condition
if central_difference:
    c[0]=2
else:
    b[0]=-1
A=tri_diag(a,b,c)
#rhs vector
d=np.repeat(-h*h*beta,n)
#rhs boundary condition
d[-1]=d[-1]-Tb
Tn=np.linalg.solve(A,d)

#append boundary temperature
Tn=np.append(Tn,Tb)
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
plt.legend()
plt.grid()
ni=n//2
yi=y[ni]
err=np.abs(Tn[ni]-analytical(yi))
print('error at point ' + str(ni)+' is='+str(err))
print(Tn)
# %%
