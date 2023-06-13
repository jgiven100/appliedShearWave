import os

import arrays.matrix as mat
import arrays.vector as vec

import newmark.newmark as newmark

import utilities.motion as motion
import utilities.save as save

import numpy as np


def solve(params, sim):
    """Solve 1D FEM problem

    Parameters
    ----------
    params : dict
        Dictionary of material parameters:
        `'vs'`: Shear wave velocity [m/s]
        `'rho'`: Mass density [kg/m3]
        `'vs_rock'`: Shear wave velocity of underlying rock [m/s]
        `'rho_rock'`: Mass density of underlying rock [kg/m3]
    sim : dict
        Dictionary of simulation settings:
        `'name'`: Name of output directory
        `'A'`: Amplitude of imposed velocity
        `'B'`: Period of imposed velocity equals 2*pi/B
        `'h'`: Height of total bar [m]
        `'h_elem'`: Height of element [m] (optional)
        `'w_elem'`: Width of element [m] (optional)
        `'l_elem'`: Length of element [m] (optional)
        `'print_flag'`: Boolean with True to print matrices terminal (optional)

    Returns
    -------
    None
    """

    # Set directory name for saving
    saveDir = 'simulation/data/' + sim['name']

    # Make directory if it does not exist
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Warn and quit if directory already exists
    else:
        print('Warning: data save location already exists!!')
        quit()

    # Change current directory to correct location
    os.chdir(saveDir)

    # Save input paramters
    d = {'Params': params, 'Sim': sim}
    save.saveDicts(d)

    # Grab mesh settings
    h = sim['h']
    h_elem = sim['h_elem'] if (sim.get('h_elem') != None) else 1.0
    w_elem = sim['w_elem'] if (sim.get('w_elem') != None) else 1.0
    l_elem = sim['l_elem'] if (sim.get('l_elem') != None) else 1.0

    # Compute helpful mesh params
    num_elem = int(h / h_elem)
    num_nodes = num_elem + 1

    # Compute cross sectional area
    area_elem = w_elem * l_elem

    # Warning and quit if total height and element height are incompatible
    if ((h % h_elem) != 0):
        print('Warning: total height and element height are incompatible!!')
        quit()

    # Grab material params
    vs = params['vs']
    rho = params['rho']
    vs_rock = params['vs_rock']
    rho_rock = params['rho_rock']

    # Compute gloabl mass, stiffness, and damping matrix
    m = mat.MassMatrix(num_nodes, rho, area_elem, h_elem)
    k = mat.StiffnessMatrix(num_nodes, vs, rho, area_elem, h_elem)
    c = mat.DampingMatrix(num_nodes, vs_rock, rho_rock, area_elem)

    # Compute gloabl force vector
    f = vec.ForceVector(num_nodes, vs_rock, rho_rock, area_elem)

    # Grab print boolean and output matrices
    p_flag = sim['pflag'] if (sim.get('print_flag') != None) else False
    if p_flag:
        m.out()
        k.out()
        c.out()
        f.out()

    # Grab kinematic parameters for base motion
    rigid = sim['rigid']
    A = sim['A']
    B = sim['B']
    base_motion = motion.Motion(A, B)

    # Set explicit Newmark params
    beta = 0.0
    gamma = 0.5

    #
    tf = 2.5
    dt = 1.0e-4

    #
    steps = int(tf / dt)
    time = np.linspace(0, tf, steps)

    # Set Newmark solver
    solver = newmark.ExplicitNewmarkCompliant(beta, gamma, dt, B, m.matrix,
                                              k.matrix, c.matrix, f)
    if rigid:
        solver = newmark.ExplicitNewmarkRigid(beta, gamma, dt, B, m.matrix,
                                              k.matrix, c.matrix, f)

    # Initialize nodes
    u = np.zeros((num_nodes, steps + 1))
    v = np.zeros((num_nodes, steps + 1))
    a = np.zeros((num_nodes, steps + 1))

    # Loop over each step
    for s, t in enumerate(time):

        # Imposed kinematics for current step
        v_hat = base_motion.v(t)
        a_hat = base_motion.a(t)

        # Solve
        utemp, vtemp, atemp = solver.solve(u[:, s], v[:, s], a[:, s], v_hat,
                                           a_hat)

        # Save current solution
        u[:, s + 1] += utemp
        v[:, s + 1] += vtemp
        a[:, s + 1] += atemp

    # Save simulation to txt for visualization
    save.saveData(u, "disp")
    save.saveData(v, "vel")
    save.saveData(a, "acc")
