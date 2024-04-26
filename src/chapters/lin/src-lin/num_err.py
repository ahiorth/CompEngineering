#%%
import numpy as np
import sympy as sym

T0,T1,T2,T3,b,g1,h,Tb=sym.symbols('T0, T1, T2, T3, b, g1, h, Tb')
f1=sym.Eq(-1*T0+1*T1+g1*h*h,-b*h*h)
f2=sym.Eq(T0-2*T1+T2,-b*h*h)
f3=sym.Eq(T1-2*T2+T3,-b*h*h)
f4=sym.Eq(T2-2*T3,-b*h*h-Tb)
sol=sym.solve([f1,f2,f3,f4],(T0,T1,T2,T3))
print(sol)
T0,T1,T2,T3,T4,T5,T6,T7,b,g1,h,Tb=sym.symbols('T0, T1, T2, T3, T4,T5,T6,T7,b, g1, h, Tb')
f1=sym.Eq(-1*T0+1*T1+g1*h*h,-b*h*h)
f2=sym.Eq(T0-2*T1+T2,-b*h*h)
f3=sym.Eq(T1-2*T2+T3,-b*h*h)
f4=sym.Eq(T2-2*T3+T4,-b*h*h)
f5=sym.Eq(T3-2*T4+T5,-b*h*h)
f6=sym.Eq(T4-2*T5+T6,-b*h*h)
f7=sym.Eq(T5-2*T6+T7,-b*h*h)
f8=sym.Eq(T6-2*T7,-b*h*h-Tb)
sol=sym.solve([f1,f2,f3,f4,f5,f6,f7,f8],(T0,T1,T2,T3,T4,T5,T6,T7))
print(sol)
# %%
