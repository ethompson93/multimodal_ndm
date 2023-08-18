'''run the network diffusion model with a weighted sum of different connectomes'''

import numpy as np
import pandas as pd
from src.mysse import mysse
from src.network_diffusion_model import ndm
from src.connectome import seed2idx

CORT_IDX = np.concatenate([np.arange(34), np.arange(49, 83)])
REF_LIST = pd.read_csv( "../data/TauRegionList.csv")["Raj_label"].tolist()

def ndm_combine_connectomes(conns, weights, data, seed_region):
    '''
    runs the networks diffusion model
        Parameters:
            conns : 
            weights : 
            data : 
            seed_region : seed region for the initial condition

        Returns:
    '''
    if len(conns) != len(weights):
        raise ValueError("there need to be the same number of connectomes and weights")

    weights=np.array(weights)
    thetas = weights/(np.sum(weights))

    combined_connectome = 0
    for theta, conn in zip(conns, thetas):
        combined_connectome += theta*(conn.load_data(thr=conn.thr))

    #set parameters for network diffusion model
    d_t = 100
    t_max = 300000

    seed_l_ind, seed_r_ind = seed2idx(seed_region, REF_LIST)
    x_0 = np.zeros(np.shape(combined_connectome)[0])
    x_0[seed_l_ind] = 1
    x_0[seed_r_ind] = 1

    #run model
    _, x_t = ndm(conn=combined_connectome,
                 x_0=x_0,
                 gamma=5e-5,
                 time = np.arange(0, t_max, d_t),
                 d_t=d_t)

    sse = mysse(x_t[CORT_IDX, :], data)
    pred = np.squeeze(x_t[:, np.argmin(sse)])
    score = np.corrcoef(pred[CORT_IDX], data)[0,1]

    return {"SSE":np.min(sse), "r":score, "prediction":pred}
