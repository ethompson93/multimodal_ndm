''' code to find an optimum weighted sum of multimodal connectomes 
	for modelling pathology spread with the network diffusion model'''
import os
import argparse
import json
import numpy as np
import pandas as pd
import skopt
from src.connectome import Connectome
from src.optimise_connectome_combo import optimise_connectome_combo
from src.data_norm import data_norm

### parse command line arguments ###
parser = argparse.ArgumentParser()
parser.add_argument('data_name',
					help="name for the data, eg. tau, atrophy")
parser.add_argument('data_path',
					help="path to the csv where the data is saved")
parser.add_argument('conn_names',
					nargs="*",
					help = "select the connectomes you want to include in the combined connectome, \
                    options = {tractography, geodesic, functional, morphological, microstructural}")
parser.add_argument('-n_iter',
					type=int,
					default=500,
					help="number of iterations for the GP minimiser (default=500)")
parser.add_argument('-n_starts',
					type=int,
					default=300,
					help="number of random initialisations for the GP minimiser (default=300)")
parser.add_argument('-seed',
					default="Inferiortemporal",
					help="seed region to initialise the network diffusion model (default=Inferiortemporal)")
args = parser.parse_args()

DATA_NAME = args.data_name
DATA_PATH = args.data_path
CONN_NAMES = args.conn_names

N_ITER = args.n_iter
N_STARTS = args.n_starts
SEED = args.seed

#for Desikan-Killiany atlas
CORT_IDX = np.concatenate([np.arange(34), np.arange(49, 83)])
####################################

DATA_DIR = "../data"
RESULTS_DIR = f"../results/optimisations/{DATA_NAME}/{SEED}"

if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

# load in the ref list
REF_LIST = pd.read_csv( f"{DATA_DIR}/TauRegionList.csv")["Raj_label"].tolist()

# load in the connectomes
sc = Connectome("tractography", f"{DATA_DIR}/connectomes/tractography.csv")
fc = Connectome("functional", f"{DATA_DIR}/connectomes/functional.csv")
geo = Connectome("geodesic", f"{DATA_DIR}/connectomes/geodesic.csv", inv=True)
morph = Connectome("morphological", f"{DATA_DIR}/connectomes/morphological.csv")
mpc = Connectome("microstructural", f"{DATA_DIR}/connectomes/microstructural.csv")

modalities = [sc, fc, geo, morph, mpc]

# read in the optimal thresholds from single modality results
with open(f"{DATA_DIR}/{DATA_NAME}_thresholds.txt") as f:
    threshold_dict = f.read()
thresholds = json.loads(threshold_dict)

for connectome in modalities:
    connectome.thr = thresholds[connectome.name]

# load in the data
df_data = pd.read_csv(DATA_PATH, index_col=0)
data_allsubs = df_data.values
data = np.mean(data_allsubs, axis=0)
data = data_norm(data)
data = data[CORT_IDX]

# choose connectomes
conns = [m for m in modalities if m.name in CONN_NAMES]

# run optimisation
best_params, results = optimise_connectome_combo(conns, data, SEED, N_ITER, N_STARTS)

# save results in a pickle file
counter = 0
connectomes = "_".join(CONN_NAMES)

filename = RESULTS_DIR + f"/{connectomes}_niter_{N_ITER}_nstart_{N_STARTS}"
filename = filename + "_{}.pkl"
while os.path.isfile(filename.format(counter)):
    counter += 1
filename = filename.format(counter)

del results.specs['args']['func'] # delete to save space
del results['models']
results['best_params'] = best_params
skopt.dump(results,filename)
