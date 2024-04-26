#%%
import work 
print ("GCD : ", work.gcd(35, 42))
  
print ("\ndivide : ", work.divide(42, 8))
  
print ("\navg : ", work.avg([1, 2, 3]))
  
p1 = work.Point(1, 2)
p2 = work.Point(4, 5)
print ("\ndistance : ", work.distance(p1, p2))

# %%

import ctypes
import os
  
# locating the 'libsample.so' file in the
# same directory as this file
_file = './libsample.so'
_path = os.path.join(*(os.path.split(__file__)[:-1] + (_file, )))
_mod = ctypes.cdll.LoadLibrary(_path)
print ("GCD : ", _mod.gcd(35, 42))
print ("\ndivide : ", _mod.divide(42, 8))
print ("\navg : ", _mod.avg([1, 2, 3]))

# %%
