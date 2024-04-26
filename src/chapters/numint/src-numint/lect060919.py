import numpy as np
# Function to be integrated
def f(x):
    return np.sin(x)

#In the implementation below the calculation goes faster 
#when we avoid unnecessary multiplications by h in the loop
def int_trapez(lower_limit, upper_limit,func,N):
    """ calculates the area of func over the domain lower_limit
        to upper limit using N integration points """
    h       = (upper_limit-lower_limit)/N
    area    = func(lower_limit)+func(upper_limit)
    area   *= 0.5
    val     = lower_limit
    for k in range(1,N): # loop over k=1,..,N-1
        val  += h # midpoint value 
        area += func(val)
    return area*h

def int_midpoint(lower_limit, upper_limit,func,N):
    """ calculates the area of func over the domain lower_limit
        to upper limit using N integration points """
    h    = (upper_limit-lower_limit)/N
    area = 0.
    for k in range(0,N): # loop over k=0,1,..,N-1
        val = lower_limit+(k+0.5)*h # midpoint value 
        area += func(val)
    return area*h     

a=0
b=np.pi

N=[4**i for i in range(10)]

print("N\t\th\t\tMidpoint\t\tTrapezoidal")
for n in N:
    print(n,(b-a)/n,2-int_midpoint(a,b,f,n),2-int_trapez(a,b,f,n),sep='\t')
