'''
Script to run the network diffusion model
 - Connectome type and threshold are set by the user
 - The output of the model is compared to a target dataset (eg. tau PET SUVRs)
 - The script saves a csv file of the Pearson's R correlation between the model 
and the data at the optimal model timepoint, for each seed region in the Desikan-Killiany atlas
'''

import os
import argparse
import numpy as np
import pandas as pd
from src.network_diffusion_model import ndm
from src.prep_connectome import prep_connectome
from src.mysse import mysse
from src.data_norm import data_norm

### parse command line arguments ###
parser = argparse.ArgumentParser()
parser.add_argument("conn_type", help="type of connectome")
parser.add_argument("conn_path", help="path to the connectome, saved as a comma delimited csv file")
parser.add_argument("thr", type=float, \
        help="threshold for the connectome - proportion of strongest weights retained [0-1]")
parser.add_argument("data_path", help="path to the target data (tau SUVRs, atrophy etc.)")
parser.add_argument("data_name", help="name of your target data, eg.tau")

args = parser.parse_args()

CONN_TYPE = args.conn_type
CONN_PATH = args.conn_path
THR = args.thr
DATA_PATH = args.data_path
DATA_NAME = args.data_name

# these are specific to the Desikan-Killiany atlas
SUBCORT_IDX=[34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 83]
CORT_IDX = np.concatenate([np.arange(34), np.arange(49, 83)])

REF_LIST = pd.read_csv( "../data/TauRegionList.csv")["Raj_label"].tolist()

####################################

def run_ndm(c_type, c_path, thr, seed_region, ref_list):
    '''
        runs the networks diffusion model
        Parameters:
            c_type : string describing the connectome type
            c_path : the path to the comma - delimited csv
                     file containing the connectom
            thr : connectome threshold
            seed_region : seed region for the initial condition
            ref_list : reference list to match the seed name to an index

        Returns:
            x_t_norm : normalised region-wise pathology timecourses
    '''
    seed_l_ind = ref_list.index(seed_region + "_L")
    seed_r_ind = ref_list.index(seed_region + "_R")

    if "geodesic" in c_type:
        conn = prep_connectome(c_path, thr=thr, inv=True, zero_neg=True)
    else:
        conn = prep_connectome(c_path, thr=thr, zero_neg=True)

    x_0 = np.zeros(np.shape(conn)[0])
    x_0[seed_l_ind] = 1
    x_0[seed_r_ind] = 1

    # set parameters for diffusion model
    gamma = 5e-5  # diffusivity constant
    d_t = 100
    t_max = 300000
    time = np.arange(0, t_max, d_t)

    #run model
    _, x_t_norm= ndm(conn, x_0, gamma, time, d_t)

    return x_t_norm

#find optimal timepoint for tau prediction and output r value
def compare(prediction, measured_pattern):

    ''' find the optimal timepoint from the model prediction 
        and return the Pearson's R correlation with the measured data
        at that timepoint '''

    sse = mysse(prediction, measured_pattern)
    pred = np.squeeze(prediction[:, np.argmin(sse)])
    corr = np.corrcoef(pred, measured_pattern)[0,1]
    return corr

# set up the path to save results
results_dir = f"../results/single_modality/{DATA_NAME}"
EXIST = os.path.exists(results_dir)
if not EXIST:
    os.makedirs(results_dir)

# load the data
df_data = pd.read_csv(DATA_PATH, index_col=0)
data_allsubs = df_data.values

seeds = [string[:-2] for string in REF_LIST]
seeds = list(set(seeds))

# deal with inclusion of subcortical values (for off-target binding etc)
data_allsubs = np.delete(data_allsubs, SUBCORT_IDX, axis=1)

# average the data across subjects and normalise
data = np.mean(data_allsubs, axis=0)
data = data_norm(data)

df = pd.DataFrame()
for seed in seeds:
    x_t = run_ndm(CONN_TYPE, CONN_PATH, THR, seed, REF_LIST)
    x_t = x_t[CORT_IDX, :]
    r = compare(x_t, data)
    df = pd.concat([df, pd.DataFrame({
             "r":r,
             "seed":seed
             }, index=[0])],ignore_index=True)

    df.to_csv(f"{results_dir}/{CONN_TYPE}_thr{THR}_av_r.csv")
