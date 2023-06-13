import numpy as np


class Motion:
    """Parent class for imposed kinematic motion

    Attributes
    ----------
    A : float
        Amplitude
    B : float
        Period is 2*pi/B
    
    Methods
    -------
    u(t)
        Return imposed displacement at time t
    v(t)
        Return imposed velocity at time t
    a(t)
        Return imposed accelration at time t
    """

    def __init__(self, A, B):
        """
        Parameters
        ----------
        A : float
            Amplitude
        B : float
            Period is 2*pi/B
        """

        self.A = A
        self.B = B

    def u(self, t, tol=1e-14):
        """Return imposed displacement at time t

        Parameters
        ----------
        t : float
            Time
        tol : float
            Tolerance (default is 1e-14)

        Returns
        -------
        u : float
            Imposed displacement
        """

        u = -(self.A * (np.sin(2 * self.B * t) - 2 * self.B * t))
        u *= 1 / (4 * self.B)
        if abs(u) < tol: u = 0.0
        return u

    def v(self, t, tol=1e-14):
        """Return imposed velocity at time t

        Parameters
        ----------
        t : float
            Time
        tol : float
            Tolerance (default is 1e-14)

        Returns
        -------
        v : float
            Imposed velocity
        """

        v = self.A * np.sin(self.B * t) * np.sin(self.B * t)
        if abs(v) < tol: v = 0.0
        return v

    def a(self, t, tol=1e-14):
        """Return imposed acceleration at time t

        Parameters
        ----------
        t : float
            Time
        tol : float
            Tolerance (default is 1e-14)

        Returns
        -------
        a : float
            Imposed acceleration
        """

        a = 2 * self.A * self.B * np.sin(self.B * t) * np.cos(self.B * t)
        if abs(a) < tol: a = 0.0
        return a