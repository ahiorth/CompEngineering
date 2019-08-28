import numpy as np
import matplotlib.pyplot as plt
import pathlib
from matplotlib import cm

##from mpl_toolkits import mplot3d
##from pINTRO_linear_regression import OLSR

if __name__ == "__main__":

    gen_figs = True
    fig_folder = pathlib.Path.cwd().joinpath('figs_python')
    print(fig_folder)

    # -----------------------------------------------------------------------
    # Define function of two variables:
    def g(x,y):
        return np.sqrt(x*x+y*y)

    # Plot function of two variables with y fixed:
    fig_fix_y = plt.figure()
    plt.xlabel(r'$x$')
    plt.ylabel(r'$z$')

    x = np.linspace(-20, 20, 1000)
    y0_values = [5, 10, 15]
    colors = ['r', 'g', 'b']
    for y0, col in zip(y0_values, colors):
        plt.plot(x, g(x, y=y0), linestyle='-', c=col, label=r'$z=g(x,{})$'.format(y0))
        plt.plot(x, (x+y0)/np.sqrt(2), linestyle='--', c=col, label=r'$z=(x+{})$'.format(y0)+r'$/\sqrt{2}$')
    plt.legend(labelspacing=0.01)
    plt.tight_layout()
    # -----------------------------------------------------------------------
    if gen_figs:
        fig_fix_y.savefig(fig_folder.joinpath('plot_fxy.png'))

    # -----------------------------------------------------------------------
    def taylor_approx(x, y, *, x0=1, y0=1):
        r0 = np.sqrt(x0**2+y0**2)
        b_x = x0/r0
        b_y = y0/r0
        print('Taylor approx.={:.4f}*x+{:.4f}*y.'.format(b_x, b_y))
        return b_x*x+b_y*y
    # -----------------------------------------------------------------------

    '''
    # -----------------------------------------------------------------------
    def linear_approx(x, y):
        # 0.4269*x+0.9343*y
        #return 1.338 + 0.657*x + 0.724*y
        return 0.703*x + 0.788*y
    # -----------------------------------------------------------------------
    '''

    # -----------------------------------------------------------------------
    # Visualize 2D surface in 3 dimensions:
    lower_lim = -20
    upper_lim= 20
    x_values = np.linspace(lower_lim, upper_lim, 1000)
    y_values = np.linspace(lower_lim, upper_lim, 1000)
    X, Y = np.meshgrid(x_values, y_values)
    Z = g(X,Y)

    fig_surface_plot = plt.figure()
    ax = fig_surface_plot.gca(projection='3d')
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    ax.set_zlabel(r'$z$')
    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)
    ax.plot_surface(X, Y, (X+Y)/np.sqrt(2), color='green')
    plt.tight_layout()
    # -----------------------------------------------------------------------
    if gen_figs:
        fig_surface_plot.savefig(fig_folder.joinpath('f_surface.png'))

    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # -----------------------------------------------------------------------

    plt.show()