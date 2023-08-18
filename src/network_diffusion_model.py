''' implementation of the network diffusion model by Raj et al. (2012), Neuron '''

import numpy as np
from scipy.linalg import expm

def ndm(conn, x_0, gamma, time, d_t):
    '''
    Calculates region-wise timecourses of pathology signal, 
    according to the network diffusion model

        Parameters:
            conn : connectome array
            x_0 : initial tau accumulation in each region
            gamma : diffusivity constant
            time : list of time points at which to predict accumulation
            d_t : step between time points

        Returns:
            x_t : regionwise timecourses of pathology (regions x n_timesteps)
            x_t_norm : normalised pathology timecourses
    '''
    n_t = len(time) # number of timepoints
    n_roi = np.shape(conn)[0] # number of brain regions

    row_degree = np.sum(conn,1)

    #construct Laplacian
    diag = np.diag(np.sum(conn,0))
    laplacian = diag - conn
    laplacian = np.diag(1/(row_degree + 2e-16))@laplacian

    #estimate tau accumulation at each time point
    x_t = np.zeros((n_roi, n_t))
    x_t[:, 0] = x_0 # set first timepoint to initial conditions

    for k_t in range(1, n_t):
        x_t[:, k_t] = expm(-gamma*laplacian*d_t) @ x_t[:,k_t-1]

    x_t_norm = x_t/np.max(x_t, axis=0)

    return x_t, x_t_norm
