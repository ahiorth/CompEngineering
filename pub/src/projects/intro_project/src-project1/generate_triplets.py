import numpy as np
import matplotlib.pyplot as plt
import pathlib
import pandas as pd

##from pINTRO_linear_regression import OLSR

if __name__ == "__main__":

    data_folder = pathlib.Path.cwd().joinpath('Input')

    xyz_files = ['xyz', 'xyz2']

    # -----------------------------------------------------------------------
    # Always use x as the smallest of the two numbers:
    for i, fn in enumerate(xyz_files):
        df = pd.read_csv(data_folder.joinpath(fn+'.dat'), sep='\t')
        fno = 'triplets' if i==0 else 'triplets2'

        file_sorted = open(str(data_folder.joinpath(fno + '.dat')), 'w')
        file_sorted.write('{}\t{}\t{}\n'.format('x','y','z'))
        for x,y,z in zip(df['x'], df['y'], df['z']):
            if x <= y:
                file_sorted.write('{:.4f}\t{:.4f}\t{:.4f}\n'.format(x,y,z))
            else:
                file_sorted.write('{:.4f}\t{:.4f}\t{:.4f}\n'.format(y,x,z))
        file_sorted.close()
    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Original files with 4 significant digits only:
    for i, fn in enumerate(xyz_files):
        df = pd.read_csv(data_folder.joinpath(fn+'.dat'), sep='\t')
        fno = 'xyz_data' if i==0 else 'xyz_data2'

        file_sorted = open(str(data_folder.joinpath(fno + '.dat')), 'w')
        file_sorted.write('{}\t{}\t{}\n'.format('x','y','z'))
        for x,y,z in zip(df['x'], df['y'], df['z']):
            file_sorted.write('{:.4f}\t{:.4f}\t{:.4f}\n'.format(x,y,z))
        file_sorted.close()
    # -----------------------------------------------------------------------