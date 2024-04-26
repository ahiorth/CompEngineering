#%%
import numba as nb
import numpy as np

@nb.jit(nopython=True)
def thomas_algorithm(l, d, u, r):
    """
    Solves a tridiagonal linear system of equations with the Thomas-algorithm.

    The code is based on pseudo-code from the following reference:

        Cheney, E. W., & Kincaid, D. R.
        Numerical mathematics and computing, 7th edition,
        Cengage Learning, 2013.

    IMPORTANT NOTES:
        - This function modifies the contents of the input matrix and rhs.
        - For Numba to work properly, we must input NumPy arrays, and not lists.

    :param l: A NumPy array containing the lower diagonal (l[0] is not used).
    :param d: A NumPy array containing the main diagonal.
    :param u: A NumPy array containing the upper diagonal (u[-1] is not used).
    :param r: A NumPy array containing the system right-hand side vector.
    :return: A NumPy array containing the solution vector.
    """
    # Allocate memory for solution
    solution = np.zeros_like(d)
    n = len(solution)

    # Forward elimination
    for k in range(1, n):
        xmult = l[k] / d[k-1]
        d[k] = d[k] - xmult*u[k-1]
        r[k] = r[k] - xmult*r[k-1]

    # Back-substitution
    solution[n-1] = r[n-1] / d[n-1]
    for k in range(n-2, -1, -1):
        solution[k] = (r[k]-u[k]*solution[k+1])/d[k]

    return solution


def extract_matrix_diagonals(dense_matrix):
    """
    Extracts the lower (l), main (d), and upper (u)
    diagonals from a dense matrix.

    :param: Input dense matrix (2D NumPy array).
    :return: A triple of 1D NumPy arrays: (l, d, u).
    """
    # Note: For Numba to work, we must be consistent about number types
    d = np.array(np.diag(dense_matrix, k=0), dtype=dense_matrix.dtype)
    u = np.zeros_like(d)
    l = np.zeros_like(d)
    u[:-1] = np.diag(dense_matrix, k=1)
    l[1:] = np.diag(dense_matrix, k=-1)
    return l, d, u


if __name__ == "__main__":

    l = np.array([-1, 1.0, 1.5, 1.0], dtype='float')
    d = np.array([-2.6]*4, dtype='float')
    u = np.array([1.0, 1.0, 1.0, -1.0], dtype='float')
    r = np.array([-240.0, 0.0, 0.0, 150.0], dtype='float')
    r2 = np.copy(r)
    assert np.array_equal(r, r2)

    import scipy as sp
    import scipy.linalg
    A = np.diag(l[1:], -1) + np.diag(d, 0) + np.diag(u[:-1], 1)
    x = sp.linalg.solve(A, r)
    print('A=', A)
    print('x_SciPy=', x)

    # NB: The Thomas algorithm modifies the input diagonals
    x = thomas_algorithm(l, d, u, r)
    print('x_thomas=', x)

    l2, d2, u2 = extract_matrix_diagonals(A)
    x2 = thomas_algorithm(l2, d2, u2, r2)
    print('x2_thomas=', x2)

# %%
