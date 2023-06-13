import numpy as np


class Vector:
    """Parent class for vector

    Attributes
    ----------
    name : str
        Empty name
    dim : int
        Dimension [dim x 1] corresponding to number of nodes
    vector : Numpy array
        Numpy array [dim x 1] for zero vector
    
    Methods
    -------
    out()
        Print name and vector contents to terminal
    """

    def __init__(self, dim):
        """
        Parameters
        ----------
        dim : int
            Dimension [dim x dim] corresponding to number of nodes
        """

        self.name = None
        self.dim = dim
        self.vector = np.zeros((dim, 1))

    def out(self):
        """Print name and vector contents to terminal

        Parameters
        ----------
        None
        """

        print(f'\n{self.name : ^70}')
        print('-' * 70)
        print(f'{self.vector}\n')


class ForceVector(Vector):
    """Child class for force vectors

    Attributes
    ----------
    name : str
        Vector name
    dim : int
        Dimension [dim x dim] corresponding to number of nodes
    c : float
        Damping coeffient

    Methods
    -------
    update(v)
        Update forcing vector based on imposed velocity
    """

    def __init__(self, dim, vs_rock, rho_rock, a_elem):
        """
        Parameters
        ----------
        dim : int
            Dimension [dim x dim] corresponding to number of nodes
        vs_rock : float
            Shear wave velocity of underlying rock [m/s]
        rho_rock : float
            Density of underlying rock [kg/m3]
        a_elem : float
            Cross section of element [m2]
        """

        Vector.__init__(self, dim)

        self.name = 'Force Vector'
        """
        WARNING:
        The `factor = 1.0` will differ based on using the "upward propogating 
        wave" motion or the "outcropng wave" motion
        """
        factor = 1.0

        self.c = factor * vs_rock * rho_rock * a_elem
        self.vector[-1, 0] += self.c

    def update(self, vel):
        """Update forcing vector based on imposed velocity

        Parameters
        ----------
        vel : float
            Imposed velocity
        """

        self.vector[-1, 0] = self.c * vel