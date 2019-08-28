import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt

from pINTRO_linear_regression import OLSR

if __name__ == "__main__":

    print('This is going to contain code for the first project in MOD510.')

    # -----------------------------------------------------------------------
    def numerical_derivative(f, x, *, method='forward', h=1.0e-4):
        """
        Function to numerically evaluate the derivative of a function f=f(x).

        :param f: Function to differentiate.
        :param x: Point at which to evaluate the derivative.
        :param method: Approximation formula to apply. Available options are
                       'forward' (default), 'backward', and 'central' finite
                       differences.
        :param h: Step size (default: 1.0e-4).
        :return: Approximate value for f'(x).
        """
        if method.upper() == 'FORWARD':
            return (f(x+h)-f(x))/h
        elif method.upper() == 'BACKWARD':
            return (f(x)-f(x-h))/h
        elif method.upper() == 'CENTRAL':
            return (f(x+h)-f(x-h))/(2*h)
        else:
            raise(NotImplementedError("Differentiation method must be one of the following: 'forward', 'backward', or 'central'."))
    # -----------------------------------------------------------------------

    '''
    # -----------------------------------------------------------------------
    # Old choice of function:
    def f(x):
        return np.exp(-x)*np.sin(x)

    def df(x):
        return np.exp(-x)*(np.cos(x)-np.sin(x))

    def df2(x):
        return -2.0*np.exp(-x)*np.cos(x)
    # -----------------------------------------------------------------------
    '''

    # -----------------------------------------------------------------------
    # Use a simple function with well-known derivative:
    def f(x):
        return np.sqrt(x**2+5.0)

    # Also define first and second derivatives of f (for later use):
    def df(x):
        return x/np.sqrt(x**2+5.0)

    def df2(x):
        return 5.0/(x**2+5.0)**(3.0/2)
    # -----------------------------------------------------------------------

    '''
    # Also plotted in pINTRO_plot_functions.py:
    # -----------------------------------------------------------------------
    fig_function = plt.figure()
    plt.grid()
    plt.xlabel(r'$x$')
    plt.ylabel(r'$y$')
    x_plot = np.linspace(0, 2, 1000)
    y_plot = f(x_plot)
    plt.plot(x_plot, y_plot)

    fig_df2 = plt.figure()
    plt.grid()
    plt.xlabel(r'$x$')
    plt.ylabel(r'$y$')
    x_plot = np.linspace(0, 2, 1000)
    y_plot = df2(x_plot)
    plt.plot(x_plot, y_plot)
    # -----------------------------------------------------------------------
    '''

    # -----------------------------------------------------------------------
    # Plot numerical errors of finite difference formulas:
    x0 = 1.0
    differentiation_methods = ('forward', 'backward', 'central')
    method_markers = ('o', '^', 's')
    h_values = np.logspace(-16, -1, 16)

    for i_meth, meth in enumerate(differentiation_methods):

        fig_error_meth = plt.figure()
        plt.title('Method={} difference'.format(meth))
        plt.grid()
        plt.xscale('log')
        plt.yscale('log')
        plt.ylim((1.0e-16, 10.0))

        # Calculate error in numerical derivative:
        fder_approx = numerical_derivative(f, x0, method=meth, h=h_values)
        eps_values = np.fabs(df(x0)-fder_approx)

        # Plot results:
        plt.scatter(h_values, eps_values, label=meth, marker=method_markers[i_meth], color='black')
    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Fit straight lines to the finite difference error plots:
    x0 = 1.0
    differentiation_methods = ('forward', 'backward', 'central')
    method_markers = ('o', '^', 's')
    h_values = np.logspace(-16, -1, 16)

    for i_meth, meth in enumerate(differentiation_methods):

        fig_error_meth = plt.figure()
        plt.title('Method={} difference'.format(meth))
        plt.grid()
        plt.xscale('log')
        plt.yscale('log')
        plt.ylim((1.0e-16, 10.0))

        # Calculate error in numerical derivative:
        fder_approx = numerical_derivative(f, x0, method=meth, h=h_values)
        eps_values = np.fabs(df(x0)-fder_approx)

        # Plot results:
        plt.scatter(h_values, eps_values, label=meth, marker=method_markers[i_meth], color='black')

        # Fit straight-line (on a log-log plot) to left part of curve:
        x_vals = np.log10(h_values[1:10])
        y_vals = np.log10(eps_values[1:10])
        a, b = OLSR(x_vals, y_vals)
        fit_left = a+b*np.log10(h_values)
        plt.plot(h_values, 10.0**fit_left, color='black', linestyle='--', label='Slope={:.2f}'.format(b))

        # Fit straight-line (on a log-log plot) to right part of curve:
        x_vals = np.log10(h_values[-5:])
        y_vals = np.log10(eps_values[-5:])
        a, b = OLSR(x_vals, y_vals)
        fit_right = a+b*np.log10(h_values)
        plt.plot(h_values, 10.0**fit_right, color='black', linestyle='-', label='Slope={:.2f}'.format(b))


        plt.legend(loc='lower left')
        plt.tight_layout()
    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Investigate truncation errors in more detail:
    h_values = np.logspace(-16, -1, 16)
    fd_values = numerical_derivative(f, x0, method='forward', h=h_values)
    abs_errors = np.fabs(df(x0)-fd_values)

    # The second derivative is monotonically decreasing near x0=1, so can
    # use value of f''(x0) for the upper bound calculation.
    # Use more points when estimating the error:
    h_val = np.logspace(-16, 1, 1000)
    max_est_errors = 0.17*h_val

    fig_error = plt.figure()
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Step size, '+'$h$')
    plt.ylabel('Error')
    plt.scatter(h_values, abs_errors, color='black', label='Actual error')
    plt.plot(h_val, max_est_errors, color='black', label='Max. est. truncation error')
    plt.legend()
    plt.tight_layout()
    # -----------------------------------------------------------------------
    '''
    def df2(x):
        return 5/(x**2+5)**(3/2)
    max_est_errors = 0.5*h_val*np.abs(df2(x0))
    '''

    # -----------------------------------------------------------------------
    machine_epsilon = np.finfo(float).eps
    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Add round-off error term:
    eps_M = 1.0e-16
    max_est_errors2 = max_est_errors + (2.0*eps_M*np.abs(f(x0)))/h_val

    fig_error2 = plt.figure()
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Step size, '+'$h$')
    plt.ylabel('Error')
    plt.scatter(h_values, abs_errors, color='black', label='Actual error')
    plt.plot(h_val, max_est_errors2, color='black', label='Max. est. total error')
    plt.legend()
    plt.tight_layout()
    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Estimate critical value of the step size (minimum point of total error):
    h_min = 2.0*np.sqrt(eps_M*np.abs(f(x0)/df2(x0)))
    print('h_min={}.'.format(h_min))

    # Same as figure 2, but with h_min indicated by a vertical bar:
    fig_error3 = plt.figure()
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Step size, '+'$h$')
    plt.ylabel('Error')
    plt.scatter(h_values, abs_errors, color='black', label='Actual error')
    plt.plot(h_val, max_est_errors2, color='black', label='Max. est. total error')
    plt.axvline(h_min, color='red', linestyle='--')
    plt.legend()
    plt.tight_layout()
    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Investigate effect of using 32-bit floating point numbers:
    h_values32 = np.array([10.0**-e for e in range(1, 17)], dtype=np.float32)
    fd_values32 = numerical_derivative(f, x0, method='forward', h=h_values32)
    abs_errors32 = np.abs(df(x0)-fd_values32)

    # 32-bit numbers require a different epsilon to estimate round-off errors:
    eps_M32 = 1.0e-8
    est_error32 = 0.5*h_val*np.abs(df2(x0))+ (2.0*eps_M32*np.abs(f(x0)))/h_val

    fig_error32 = plt.figure()
    plt.title('Impact of floating point number representation')
    plt.ylim((1.0e-10, 1.0))
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Step size, '+'$h$')
    plt.ylabel('Error')
    plt.scatter(h_values, abs_errors, color='black', marker='o', label='Error (64-bit)')
    plt.scatter(h_values32, abs_errors32, color='red', marker='s', label='Error (32-bit)')
    plt.plot(h_val, est_error32, color='black', label='Est. error (32-bit)')
    plt.legend(loc='lower left')
    plt.tight_layout()
    # -----------------------------------------------------------------------

    plt.show()
