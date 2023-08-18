import numpy as np
from src.prep_connectome import prep_connectome
from src.network_diffusion_model import ndm

def seed2idx(seed, ref_list):
    seed_l_ind = ref_list.index(seed + "_L")
    seed_r_ind = ref_list.index(seed + "_R")
    return (seed_l_ind, seed_r_ind)

class Connectome:
    def __init__(self, name, path, ref_list, thr=0.1, inv=False, seed=False, gamma=1):
        self.name = name
        self.path = path
        self.ref_list = ref_list
        self.thr = thr
        self.inv = inv
        self.seed = seed
        self.gamma = gamma

    def load_data(self, thr):
        C = prep_connectome(self.path, thr, gm=True, inv=self.inv)
        return C
