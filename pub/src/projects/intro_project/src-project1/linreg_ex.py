import numpy as np
import scipy as sp
import scipy.optimize
import scipy.special
import pandas as pd
import matplotlib.pyplot as plt
import pathlib
import statsmodels.api as sm
import sklearn.datasets
from sklearn.linear_model import LinearRegression

from pINTRO_linear_regression import OLSR, OLSR_multiple, OLSR_multiple_predict

if __name__ == "__main__":

    plt.style.use('grayscale')

    # Examples from the book "Applying Regression and Correlation"
    # by Jeremy Miles and  Mark Shevlin.

    input_folder = pathlib.Path.cwd().joinpath('Input')

    # -----------------------------------------------------------------------
    # Data for (multiple) linear regression:
    data = pd.read_csv(input_folder.joinpath('grades.dat'), sep='\t')
    books = data['books']
    attend = data['attend']
    grades = data['grade']
    N = len(grades)

    # Perform simple linear regression:
    a, b = OLSR(books, grades)
    print('-------------------- Simple linear regression--------------------')
    print('y={:.3f}+{:.3f}*x.'.format(a, b))

    predicted_grades= a + b*books
    mean_predicted_grades = np.mean(predicted_grades)
    print('mean predicted grade=' , mean_predicted_grades)
    mean_std = np.sqrt(np.sum((predicted_grades-mean_predicted_grades)**2)/(N-1))
    mean_var = mean_std**2
    print('sample standard deviation of mean={:.2f}, variance={:.2f}.'.format(mean_std,mean_var))
    residuals = grades - predicted_grades
    residual_std = np.sqrt(np.sum((residuals-np.mean(residuals))**2)/(N-1))
    residual_var = residual_std**2
    print('sample standard deviation of residual={:.2f}, variance={:.2f}'.format(residual_std, residual_var))
    explained_variance = mean_var/(mean_var+residual_var)
    print('explained variance={:.3f}.'.format(explained_variance))
    print('Correlation coefficient={:.3f}.'.format(np.sqrt(explained_variance)))

    fig_grade_vs_books = plt.figure()
    plt.xlabel('Number of books read')
    plt.ylabel('Achieved grade')
    plt.scatter(books, grades, marker='o')
    plt.plot(books, a+b*books, color='black', linestyle='-')

    # Perform multiple linear regression:
    print('-------------------- Multiple linear regression--------------------')
    matrix =  np.array([books, attend]).transpose()
    regr_coeffs = OLSR_multiple(matrix, grades)
    grades_pred = OLSR_multiple_predict(matrix, regr_coeffs)
    mean_std = np.sqrt((np.sum((grades_pred-np.mean(grades_pred))**2))/(N-1))
    mean_var = mean_std**2
    residuals = grades - grades_pred
    residual_std = np.sqrt((np.sum((residuals-np.mean(residuals))**2))/(N-1))
    residual_var = residual_std**2
    explained_variance = mean_var/(mean_var+residual_var)
    print('y={:.3f}+{:.3f}*books+{:.3f}*attend'.format(regr_coeffs[0], regr_coeffs[1], regr_coeffs[2]))
    print('Explained variance=R^2={:.3f}.'.format(explained_variance))
    # ----------------------------------------------------------------------

    plt.show()