import numpy as np
import matplotlib.pyplot as plt


def textSettings():
    """Make text look pretty
    
    Parameters
    ----------
    None

    Returns 
    -------
    None
    """

    font = 'cmr10'
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = [font] + plt.rcParams['font.serif']
    plt.rcParams['mathtext.fontset'] = 'cm'
    plt.rcParams['axes.formatter.use_mathtext'] = True
    plt.rcParams['font.size'] = 8


def legendDict(loc=1):
    """Dictionary of legend settings

    Parameters
    ----------
    loc : int
        Location integer (default is 1)

    Returns
    -------
    tDict : dict
        Dictionary of legend settings
    """

    lDict = {
        'loc': loc,
        'fancybox': False,
        'edgecolor': '0.0',
        'fontsize': 7,
        'framealpha': 1.0,
    }

    return lDict


def tickDict():
    """Dictionary of tick settings

    Parameters
    ----------
    None

    Returns
    -------
    tDict : dict
        Dictionary of tick settings
    """

    tDict = {
        'which': 'both',
        'direction': 'in',
        'top': True,
        'right': True,
    }

    return tDict