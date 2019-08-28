from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("rk4_2.pyx")
)
