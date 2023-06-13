import numpy as np


class Matrix:
    """Parent class for matrices

    Attributes
    ----------
    name : str
        Empty name
    dim : int
        Dimension [dim x dim] corresponding to number of nodes
    matrix : Numpy array
        Numpy array [dim x dim] for zero matrix
    
    Methods
    -------
    out()
        Print name and matrix contents to terminal
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
        self.matrix = np.zeros((dim, dim))

    def out(self):
        """Print name and matrix contents to terminal

        Parameters
        ----------
        None
        """

        print(f'\n{self.name : ^70}')
        print('-' * 70)
        print(f'{self.matrix}\n')


class DampingMatrix(Matrix):
    """Child class for damping matrices

    Attributes
    ----------
    name : str
        Matrix name
    dim : int
        Dimension [dim x dim] corresponding to number of nodes
    c : float
        Damping coeffient
    matrix : Numpy array
        Numpy array [dim x dim] for dammping matrix
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

        Matrix.__init__(self, dim)

        self.name = 'Damping Matrix'
        self.c = vs_rock * rho_rock * a_elem
        self.matrix[-1, -1] += self.c


class MassMatrix(Matrix):
    """Child class for mass matrices

    Attributes
    ----------
    name : str
        Matrix name
    dim : int
        Dimension [dim x dim] corresponding to number of nodes
    mass : float
        Element mass [kg]
    matrix : Numpy array
        Numpy array [dim x dim] for lumped mass matrix
    """

    def __init__(self, dim, rho, h_elem, a_elem):
        """
        Parameters
        ----------
        dim : int
            Dimension [dim x dim] corresponding to number of nodes
        rho : float
            Mass density [kg/m3]
        h_elem : float
            Height of element [m]
        a_elem : float
            Cross section of element [m2]
        """

        Matrix.__init__(self, dim)

        self.name = 'Mass Matrix'
        self.mass = rho * h_elem * a_elem
        for i in range(dim - 1):
            self.matrix[i, i] += 0.5 * self.mass
            self.matrix[i + 1, i + 1] += 0.5 * self.mass


class StiffnessMatrix(Matrix):
    """Child class for stiffness matrices

    Attributes
    ----------
    name : str
        Stiffness name
    dim : int
        Dimension [dim x dim] corresponding to number of nodes
    G : float
        Shear modulus [Pa]
    g : float
        Shear spring constant
    matrix : Numpy array
        Numpy array [dim x dim] for stiffness matrix
    """

    def __init__(self, dim, vs, rho, a_elem, h_elem):
        """
        Parameters
        ----------
        dim : int
            Dimension [dim x dim] corresponding to number of nodes
        vs : float
            Shear wave velocity [m/s]
        rho : float
            Mass density [kg/m3]
        a_elem : float
            Cross section of element [m2]
        h_elem : float
            Height of element [m]
        """

        Matrix.__init__(self, dim)

        self.name = 'Stiffness Matrix'
        self.G = vs * vs * rho
        self.g = self.G * a_elem / h_elem
        matrix_elem = self.g * np.array([
            [1.0, -1.0],
            [-1.0, 1.0],
        ])
        for i in range(dim - 1):
            self.matrix[i:i + 2, i:i + 2] += matrix_elem