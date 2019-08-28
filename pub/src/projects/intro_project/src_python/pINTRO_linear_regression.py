import numpy as np
import scipy as sp
import scipy.optimize
import scipy.special
import pandas as pd
import matplotlib.pyplot as plt
import pathlib
from sklearn.linear_model import LinearRegression

# -----------------------------------------------------------------------
def OLSR(x, y):
    """
    Custom implementation of Ordinary Least Squares Regression.

    :param x: Input data points for the independent variable (array)
    :param y: Input data points for the dependent variable (array)
    :return: Tuple consisting of (intercept, slope) of the regression line.
    """
    x_avg = np.mean(x)
    y_avg = np.mean(y)
    fac1 = np.sum((x-x_avg)*(y-y_avg))
    fac2 = np.sum((x-x_avg)**2)
    slope = fac1/fac2
    intercept = y_avg - slope*x_avg
    return intercept, slope
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
def OLSR_multiple(X_matrix, y, *, include_constant_term=True):
    """
    Custom implementation of Ordinary Least Squares Regression for
    multiple predictor variables.

    This routine computes the 'best fit' regression coefficients from
    training data.

    :param X_matrix: Matrix holding values of predictor variables.
              Each column corresponds to a single variable, and the rows
              correspond to different observations.
    :param y: Input data for the dependent variable (a single array)
    :param include_constant_term: If False, force linear model to pass through
                                  the origin (no intercept term).
    :return: Array consisting of fitted coefficients to the regression line.
    """
    num_rows, num_cols = X_matrix.shape
    X = np.c_[np.ones(num_rows), X_matrix]  # add column of ones
    X = X if include_constant_term else X_matrix
    X_T = X.transpose()
    A = X_T.dot(X)
    b = X_T.dot(y)
    lsq_sol = sp.linalg.solve(A, b)
    return lsq_sol
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
def OLSR_multiple_predict(X_matrix, beta_coeffs, *, include_constant_term=True):
    """
    Custom implementation of Ordinary Least Squares Regression for
    multiple predictor variables.

    This routine predicts values of the independent variable based on
    known input for the predictor variables, and knowing the 'best-fit'
    regression coefficients.

    :param X_matrix: Matrix holding values of predictor variables.
              Each column corresponds to a single variable, and the rows
              correspond to different observations.
    :param beta_coeffs: Fitted regression coefficients (from training data).
    :param include_constant_term: If False, force linear model to pass through
                                  the origin (no intercept term).
    :return: Array consisting of predicted y-values for the given input.
    """
    num_rows, num_cols = X_matrix.shape
    X = np.c_[np.ones(num_rows), X_matrix]  # add column of ones
    X = X if include_constant_term else X_matrix
    y_pred = np.dot(X, beta_coeffs)
    return y_pred
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
def calc_r_squared(y_obs, y_pred):
    """
    Calculates R^2 for a linear regression model.

    :param y_obs: Array of observed values.
    :param y_pred: Array of corresponding predicted / calculated values.
    :return: Coefficient of deterermination (R^2) for the fit.
    """
    return 1.0 - np.sum((y_obs-y_pred)**2)/np.sum((y_obs-np.mean(y_obs))**2)
# -----------------------------------------------------------------------


if __name__ == "__main__":

    generate_figs = True

    # Place to store figures that are later included in .do.txt file:
    fig_folder = pathlib.Path.cwd().joinpath('figs_python')

    # -----------------------------------------------------------------------
    # Test least squares routine:
    x = np.linspace(0, 1, 50)
    y = 3*x + 2
    alpha, beta = OLSR(x, y)
    print('Slope={0}, intercept={1}.'.format(beta, alpha))
    # -----------------------------------------------------------------------

    '''
    # -----------------------------------------------------------------------
    # Plot GPA scores versus SAT scores:
    plt.style.use('grayscale')
    input_folder = pathlib.Path.cwd().joinpath('Input')
    data_file = str(input_folder.joinpath('sat_gpa.dat'))
    df = pd.read_csv(data_file, sep='\t')
    x = df['SAT'].values
    y = df['GPA'].values
    a, b = OLSR(x, y)

    fig_gpa_sat = plt.figure()
    plt.xlabel('SAT')
    plt.ylabel('GPA')
    plt.scatter(x, y)
    plt.plot(x, a+b*x, color='black', linestyle='-')
    plt.tight_layout()
    # -----------------------------------------------------------------------
    if generate_figs:
        fig_gpa_sat.savefig(fig_folder.joinpath('OLS.png'))

    # -----------------------------------------------------------------------
    # Compare different implementations of linear regression:
    x = df['SAT'].values
    y = df['GPA'].values

    # Custom implementation:
    a, b = OLSR(x, y)
    fit_y1 = a+b*x

    # Scikit-learn:
    model = LinearRegression()
    x_vals = x.reshape(-1, 1)
    model.fit(x_vals, y)
    a2, b2 = model.intercept_, model.coef_[0]
    fit_y2 = model.predict(x_vals)

    # numpy.polyfit:
    coeffs_polyfit = np.polyfit(x, y, deg=1)
    a3, b3 = coeffs_polyfit[1], coeffs_polyfit[0]
    fit_y3 = a3+b3*x

    print('Regression line found using custom implementation: {:.5f}*x+{:.5f}.'.format(b,a))
    print('Regression line found using scikit-learn: {:.5f}*x+{:.5f}.'.format(b2,a2))
    print('Regression line found using numpy.polyfit: {:.5f}*x+{:.5f}.'.format(b3, a3))
    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Compute r-squared for the previous example:
    r_sq = calc_r_squared(y, fit_y1)
    print('r_squared for custom implementation={:.3f}.'.format(r_sq))
    print('Correlation coefficient={:.3f}'.format(np.sqrt(r_sq)))

    # Check using scikit-learn calculation:
    r2 = model.score(x_vals, y)
    print('r_squared for scikit-learn implementation={:.3f}.'.format(r2))
    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Plot residuals for the simple linear regression:
    fig_residual_plot = plt.figure()
    plt.xlabel('SAT')
    plt.ylabel('Residual')
    plt.scatter(x, y-fit_y1)
    plt.axhline(0, linestyle='--', color='black')
    # -----------------------------------------------------------------------
    '''

    # -----------------------------------------------------------------------
    # Test multiple linear regression routine for a known linear function:

    # Here: Each column of X corr. to a single predictor variable:
    X = np.array([[1, 1], [1, 2], [2,2], [2,3]])
    y = np.dot(X, np.array([1,2]))+3  # y = 3 + x1 + 2*x2
    regr_coeffs = OLSR_multiple(X, y)
    b0, b1, b2 = regr_coeffs[0], regr_coeffs[1], regr_coeffs[2]
    y_pred = OLSR_multiple_predict(X, regr_coeffs)
    print('y_pred should equal y, because y is an exact linear function of x1 and x2.')
    print('y:', y)
    print('y_pred:', y_pred)
    r2 = calc_r_squared(y, y_pred)
    print('Regression coefficients for custom implementation: {:.1f}, {:.1f}, {:.1f} (R2={:.1f}).'.format(b0, b1, b2, r2))
    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Investigate xyz.dat:
    input_folder = pathlib.Path.cwd().joinpath('Input')
    fn_triplets = 'xyz_data'  # triplets, xyz, xyz_data
    data_file = str(input_folder.joinpath(fn_triplets+'.dat'))
    data_tests = pd.read_csv(data_file, sep='\t')

    # z as a function of x:
    x = data_tests['x']
    z = data_tests['z']
    a1, b1 = OLSR(x, z)
    z_pred = a1+b1*x
    rho_xz = np.sqrt(calc_r_squared(z, z_pred))

    fig_xz = plt.figure()
    plt.title('Correlation coefficient={:.3f}.'.format(rho_xz))
    plt.xlabel(r'$x$')
    plt.ylabel(r'$z$')
    plt.scatter(x, z)
    plt.plot(x, z_pred)

    # z as a function of y:
    y = data_tests['y']
    a2, b2 = OLSR(y, z)
    z_pred = a2+b2*y
    rho_yz = np.sqrt(calc_r_squared(z, z_pred))

    fig_yz = plt.figure()
    plt.title('Correlation coefficient={:.3f}.'.format(rho_yz))
    plt.xlabel(r'$y$')
    plt.ylabel(r'$z$')
    plt.scatter(y, z)
    plt.plot(y, z_pred)

    # Also: y as a function of x:
    a3, b3 = OLSR(x, y)
    y_pred = a3+b3*x
    rho_xy = np.sqrt(calc_r_squared(y, y_pred))
    fig_xy = plt.figure()
    plt.title('Correlation coefficient={:.3f}.'.format(rho_xy))
    plt.xlabel(r'$x$')
    plt.ylabel(r'$y$')
    plt.scatter(x, y)
    plt.plot(x, y_pred)
    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Compare custom implementation with already available functions:

    # Scikit-learn:
    model = LinearRegression()
    x_vals = x.values.reshape(-1, 1)
    model.fit(x_vals, z)
    a1_s, b1_s = model.intercept_, model.coef_[0]
    fit_xz = model.predict(x_vals)

    # numpy.polyfit:
    coeffs_polyfit = np.polyfit(x, z, deg=1)
    a1_p, b1_p = coeffs_polyfit[1], coeffs_polyfit[0]
    fit_xz = a1+b1*x

    print('Correlation between x and z:')
    print('Regression line found using custom implementation: {:.5f}*x+{:.5f}.'.format(b1,a1))
    print('Regression line found using scikit-learn: {:.5f}*x+{:.5f}.'.format(b1_s,a1_s))
    print('Regression line found using numpy.polyfit: {:.5f}*x+{:.5f}.'.format(b1_p, a1_p))

    # and similarly for the others...
    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Fit a multiple linear regression model to the xyz-data:
    const_term = False
    xy_matrix = np.array([x, y]).transpose()
    regr_coeffs = OLSR_multiple(xy_matrix, z, include_constant_term=const_term)
    b0 = regr_coeffs[0] if const_term else 0.0
    b1 = regr_coeffs[1] if const_term else regr_coeffs[0]
    b2 = regr_coeffs[2] if const_term else regr_coeffs[1]
    #b0, b1, b2 = regr_coeffs[0], regr_coeffs[1], regr_coeffs[2]
    z_pred = b0 + b1*x + b2*y
    r2 = calc_r_squared(z, z_pred)
    print('Fitted linear model: z={:.3f}+{:.3f}*x+{:.3f}*y (R2={:.3f}).'.format(b0, b1, b2, r2))
    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Use fitted linear model to predict z-values for a new data set:
    data_file = str(input_folder.joinpath(fn_triplets+'2.dat'))
    xyz_data2 = pd.read_csv(data_file, sep='\t')
    x = xyz_data2['x']
    y = xyz_data2['y']
    z = xyz_data2['z']
    xy_matrix = np.array([x, y]).transpose()
    z_pred = OLSR_multiple_predict(xy_matrix, regr_coeffs, include_constant_term=const_term)
    r2_score = calc_r_squared(z, z_pred)

    fig_prediction = plt.figure()
    plt.title(r'$r^2=$' + ' {:.3f}.'.format(r2_score))
    plt.xlabel('Predicted ' + r'$z$')
    plt.ylabel('Actual ' + r'$z$')
    plt.scatter(z_pred, z)
    plt.plot(z_pred, z_pred, linestyle='--', color='black')
    # -----------------------------------------------------------------------
    # regr_coeffs2 = np.array([1.0/np.sqrt(2)]*2)

    # -----------------------------------------------------------------------
    # Make a residual plot for z-prediction:
    residuals = z-z_pred
    fig_residuals = plt.figure()
    plt.xlabel('Fitted z-value')
    plt.ylabel('Residual')
    plt.axhline(0, linestyle='--', color='black')
    plt.scatter(z_pred, residuals)
    print('R2=', r2_score)
    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Test for a simple functional relationship z=z(x,y):
    input_folder = pathlib.Path.cwd().joinpath('Input')
    data_file = str(input_folder.joinpath('xyz.dat'))
    data_tests = pd.read_csv(data_file, sep='\t')
    x = data_tests['x']
    y = data_tests['y']
    z = data_tests['z']
    z_calc = np.sqrt(x**2+y**2)
    diff = z-z_calc
    max_diff = max(diff)
    print('Maximal difference between reported and calculated z-values: {}.'.format(max_diff))
    # -----------------------------------------------------------------------


    # -----------------------------------------------------------------------
    # Draw random x and y values that are negative:
    N = 50
    x = np.random.uniform(-20, 0, N)
    y = np.random.uniform(-20, 0, N)
    z = np.sqrt(x*x+y*y)
    xy_matrix = np.array([x, y]).transpose()
    z_pred = OLSR_multiple_predict(xy_matrix, regr_coeffs, include_constant_term=const_term)
    r2_score = calc_r_squared(z, z_pred)

    fig_prediction = plt.figure()
    plt.title(r'$r^2=$' + ' {:.3f}.'.format(r2_score))
    plt.xlabel('Predicted ' + r'$z$')
    plt.ylabel('Actual ' + r'$z$')
    plt.scatter(z_pred, z)
    plt.plot(z_pred, z_pred, linestyle='--', color='red')
    # -----------------------------------------------------------------------


    plt.show()
