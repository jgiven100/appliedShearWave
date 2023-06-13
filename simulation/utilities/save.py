import numpy as np


def saveData(df, name):
    """Save simulation data

    Parameters
    ----------
    df : array
        Numpy array [dim x steps]
    name : str
        File name

    Returns
    -------
    None
    """

    fname = f'{name}Data.txt'
    np.savetxt(fname, df, fmt='%.12f', delimiter=' ')


def saveDicts(d):
    """Save dictionary as text file

    Parameters
    ----------
    d : dict
        Dictionary of dictionaries with various input settings

    Returns
    -------
    None
    """

    for key in d:

        fname = f'save{key}.txt'
        f = open(fname, 'w')
        f.write(str(d[key]))
        f.close()