import numpy as np


class Newmark:
    """Parent class for newmark solvers

    Attributes
    ----------
    beta : float
        beta parameter
    gamma : float
        gamma parameter
    dt : float
        Time step
    time : float
        Current time
    B : float
        Period of imposed velocity equal 2*pi/B
    m : Numpy array
        Numpy array [dim x dim] for mass matrix
    k : Numpy array
        Numpy array [dim x dim] for stiffness matrix
    c : Numpy array
        Numpy array [dim x dim] for damping matrix
    f : Vector object
        Forcing vector object
    """

    def __init__(self, beta, gamma, dt, B, m, k, c, f):
        """
        Parameters
        ----------
        beta : float
            beta parameter
        gamma : float
            gamma parameter
        dt : float
            Time step
        B : float
            Period of imposed velocity equal 2*pi/B
        m : Numpy array
            Numpy array [dim x dim] for mass matrix
        k : Numpy array
            Numpy array [dim x dim] for stiffness matrix
        c : Numpy array
            Numpy array [dim x dim] for damping matrix
        f : Vector object
            Forcing vector object
        """

        self.beta = beta
        self.gamma = gamma
        self.dt = dt
        self.time = 0.0
        self.B = B
        self.m = m
        self.k = k
        self.c = c
        self.f = f


class ExplicitNewmarkCompliant(Newmark):
    """Child class for explicit newmark solver with compliant base

    Attributes
    ----------
    beta : float
        beta parameter
    gamma : float
        gamma parameter
    dt : float
        Time step
    time : float
        Current time
    B : float
        Period of imposed velocity equal 2*pi/B
    m : Numpy array
        Numpy array [dim x dim] for mass matrix
    k : Numpy array
        Numpy array [dim x dim] for stiffness matrix
    c : Numpy array
        Numpy array [dim x dim] for damping matrix
    f : Vector object
        Forcing vector object

    Methods
    -------
    solve(u, v, a, v_hat, a_hat)
        Solve for updated nodal displacement, velocity, and acceleration
    """

    def __init__(self, beta, gamma, dt, B, m, k, c, f):
        """
        Parameters
        ----------
        beta : float
            beta parameter
        gamma : float
            gamma parameter
        dt : float
            Time step
        B : float
            Period of imposed velocity equal 2*pi/B
        m : Numpy array
            Numpy array [dim x dim] for mass matrix
        k : Numpy array
            Numpy array [dim x dim] for stiffness matrix
        c : Numpy array
            Numpy array [dim x dim] for damping matrix
        f : Vector object
            Forcing vector object
        """

        Newmark.__init__(self, beta, gamma, dt, B, m, k, c, f)

    def solve(self, u, v, a, v_hat, a_hat):
        """Solve for updated nodal displacement, velocity, and acceleration

        Parameters
        ----------
        u : Numpy array
            Numpy array [dim x 1] for displacement at step `n`
        v : Numpy array
            Numpy array [dim x 1] for velocity at step `n`
        a : Numpy array
            Numpy array [dim x 1] for acceleration at step `n`
        v_hat : float
            Imposed velocity at step `n + 1`
        a_hat : float
            Imposed acceleration at step `n + 1`

        Returns
        -------
        u_update : Numpy array
            Numpy array [dim x 1] for displacement at step `n + 1`
        v_update : Numpy array
            Numpy array [dim x 1] for velocity at step `n + 1`
        a_update : Numpy array
            Numpy array [dim x 1] for acceleration at step `n + 1`
        """

        # Only impose 1/2 period of movement
        if self.time > ((1.0 * np.pi) / self.B): v_hat = 0

        # Reshape
        num_nodes = u.shape[0]
        u = u.reshape((num_nodes, 1))
        v = v.reshape((num_nodes, 1))
        a = a.reshape((num_nodes, 1))

        # Predictor
        u_temp = u + self.dt * v + 0.5 * self.dt * self.dt * a
        v_temp = v + (1 - self.gamma) * self.dt * a

        # Set RHS and LHS
        self.f.update(v_hat)
        rhs = self.f.vector - 1.0 * (self.c @ v_temp + self.k @ u_temp)
        lhs = self.m + self.gamma * self.dt * self.c

        # Solve
        a_update = (np.linalg.inv(lhs) @ rhs)[:, 0]

        # Update predictors
        v_update = v_temp[:, 0] + self.gamma * self.dt * a_update
        u_update = u_temp[:, 0]

        # Update time
        self.time += self.dt

        return u_update, v_update, a_update


class ExplicitNewmarkRigid(Newmark):
    """Child class for explicit newmark solver with rigid base

    Attributes
    ----------
    beta : float
        beta parameter
    gamma : float
        gamma parameter
    dt : float
        Time step
    time : float
        Current time
    B : float
        Period of imposed velocity equal 2*pi/B
    m : Numpy array
        Numpy array [dim x dim] for mass matrix
    k : Numpy array
        Numpy array [dim x dim] for stiffness matrix
    c : Numpy array
        Numpy array [dim x dim] for damping matrix
    f : Vector object
        Forcing vector object

    Methods
    -------
    solve(u, v, a, v_hat, a_hat)
        Solve for updated nodal displacement, velocity, and acceleration
    """

    def __init__(self, beta, gamma, dt, B, m, k, c, f):
        """
        Parameters
        ----------
        beta : float
            beta parameter
        gamma : float
            gamma parameter
        dt : float
            Time step
        B : float
            Period of imposed velocity equal 2*pi/B
        m : Numpy array
            Numpy array [dim x dim] for mass matrix
        k : Numpy array
            Numpy array [dim x dim] for stiffness matrix
        c : Numpy array
            Numpy array [dim x dim] for damping matrix
        f : Vector object
            Forcing vector object
        """

        Newmark.__init__(self, beta, gamma, dt, B, m, k, c, f)

    def solve(self, u, v, a, v_hat, a_hat):
        """Solve for updated nodal displacement, velocity, and acceleration

        Parameters
        ----------
        u : Numpy array
            Numpy array [dim x 1] for displacement at step `n`
        v : Numpy array
            Numpy array [dim x 1] for velocity at step `n`
        a : Numpy array
            Numpy array [dim x 1] for acceleration at step `n`
        v_hat : float
            Imposed velocity at step `n + 1`
        a_hat : float
            Imposed acceleration at step `n + 1`

        Returns
        -------
        u_update : Numpy array
            Numpy array [dim x 1] for displacement at step `n + 1`
        v_update : Numpy array
            Numpy array [dim x 1] for velocity at step `n + 1`
        a_update : Numpy array
            Numpy array [dim x 1] for acceleration at step `n + 1`
        """

        # Only impose 1/2 period of movement
        if self.time > ((1.0 * np.pi) / self.B): a_hat = 0

        # Reshape
        num_nodes = u.shape[0]
        u = u.reshape((num_nodes, 1))
        v = v.reshape((num_nodes, 1))
        a = a.reshape((num_nodes, 1))

        # Predictor
        u_temp = u + self.dt * v + 0.5 * self.dt * self.dt * a
        v_temp = v + (1 - self.gamma) * self.dt * a

        # Set RHS and LHS
        rhs = -1.0 * (self.k @ u_temp)
        lhs = self.m

        # Impose known acceleration
        lhs[-1, -1] = 1.0
        rhs[-1, 0] = a_hat

        # Solve
        a_update = (np.linalg.inv(lhs) @ rhs)[:, 0]

        # Update predictors
        v_update = v_temp[:, 0] + self.gamma * self.dt * a_update
        u_update = u_temp[:, 0]

        # Update time
        self.time += self.dt

        return u_update, v_update, a_update