%load_ext Cython

%%cython
def fib_cython(n):
    if n<2:
        return n
    return fib_cython(n-1)+fib_cython(n-2)
