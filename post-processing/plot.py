import os
from os.path import dirname as up

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

from settings import *


def plot(save, dir_name):
    """Displacement, velocity, and accerlation plot

    Parameters
    ----------
    save : bool
        Boolean with True to save png of figure
    dir_name : str
        Name of subdirectory where output data is located

    Returns
    -------
    None    
    """

    # Put simulation data into arrays
    inDir = up(up(up(os.getcwd()))) + '/simulation/data/' + dir_name
    u = np.loadtxt(inDir + 'dispData.txt', delimiter=' ')
    v = np.loadtxt(inDir + 'velData.txt', delimiter=' ')
    a = np.loadtxt(inDir + 'accData.txt', delimiter=' ')

    # Make matplotlib text look nice
    textSettings()

    #
    num_nodes = u.shape[0]
    steps = u.shape[1]
    t = np.linspace(0, 2.0, steps)

    # Set colormap
    c = plt.cm.copper(np.linspace(1.0, 0.25, num_nodes))

    # Make axes object
    _, axs = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(7, 8))

    # Generate labels
    labels = ['50m (Top)']
    for i in range(num_nodes - 2):
        j = abs(num_nodes - 2 - i)
        labels += [f'{j:d}m']
    labels += ['0m (Base)']

    # Plot 1D model outputs
    for i in [0, 10, 20, 30, 40, 50]:
        # for i in range(num_nodes):
        j = abs(num_nodes - 1 - i)
        axs[0].plot(t, u[j, :], label=labels[j], c=c[j])
        axs[1].plot(t, v[j, :], label=labels[j], c=c[j])
        axs[2].plot(t, a[j, :], label=labels[j], c=c[j])

    # Loop axes
    for ax in axs:

        # Set ticks
        ax.tick_params(**tickDict())
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())

        # Set legend
        ax.legend(**legendDict(0))

    # Label axes
    axs[0].set_ylabel('Displacement (x-dir) [m]')
    axs[1].set_ylabel('Velocity (x-dir) [m/s]')
    axs[2].set_ylabel(r'Acceleration (x-dir) [m/s$^2$]')
    axs[2].set_xlabel('Time [sec.]')

    # Save or show
    plt.tight_layout()
    if save:
        # TODO
        plt.savefig('kinematic.png', dpi=500)
        plt.close()
    else:
        plt.show()
