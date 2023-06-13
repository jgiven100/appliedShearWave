import numpy as np
import solve


def main():
    """
    params is a dictionary of material parameters
        'vs': Shear wave velocity [(]m/s]
        'rho': Mass density [km/m3]
        'vs_rock': Shear wave velocity of underlying rock [(]m/s]
        'rho_rock': Mass density of underlying rock [km/m3]
    """
    params = {
        'vs': 350,
        'rho': 2000,
        'vs_rock': 1500,
        'rho_rock': 2400,
    }
    """
    sim is a dictionary of simulation settings
        'name': Name of output directory
        'rigid': Boolean with True to use rigid base
        'A': Amplitude of imposed velocity
        'B': Period of imposed velocity equal 2*pi/B
        'h': Height of total bar [m]
        'h_elem': Height of element [m] (optional)
        'w_elem': Width of element [m] (optional)
        'l_elem': Length of element [m] (optional)
        'print_flag': Boolean with True to print matrices terminal (optional)
    """
    sim = {
        'name': 'compliant/',
        'rigid': False,
        'A': 0.5,
        'B': 5 * np.pi,
        'h': 25.0,
    }

    # Solve
    solve.solve(params, sim)


if __name__ == '__main__':
    main()